# Bash Playground solution

We ssh into the server:

```
ssh guest@bp.heltsikker.no
```

If you try different commands you'll notice we are in a very restricted shell. With tab completion you might find that there is a file named /flag.txt. From the challenge description as well as try/fail we realize the only available commands are the ones built into bash.

Google or experience tells us we can read a file using only bash like so:

```
while read p; do echo $p; done < /flag.txt
```

And the flag is echoed!
