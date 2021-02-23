# SECCOMP2ABYSS

You get the full source for this one, it's pretty clean and simple. It's not a hard challenge, but might be daunting for beginners, which was the intention.

We use libseccomp to reduce available system calls and simply map your shellcode and run it. The cookie cutter way to solve this is a simple open/read/write payload.
