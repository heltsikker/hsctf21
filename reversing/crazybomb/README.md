# Crazybomb

This challenge has 3 stages, each gives a flag. One is easy, one is medium and one is hard/insane. 
You *can* script your way to victory, but this challenge really requires you to do a lot of patching and strip away anti-debugging techniques.

## Stage 1

The first stage is easy, because you can complete this one by static analysis, so you dont need to worry about the anti-debugging in place. 

You need to login at the prompt. The password can be found with a string search on the binary. 
The twist here is, that the username is not shown, so through static analysis, you can look at the strcmp and see that the username is `gordon`
(Open the binary in whatever tool and search for references to `strncmp`. 



## Stage 2

In stage 2, you have to enter the right codes to prevent the bomb from going off.
You can script the input (its just simple calculations), but you cant nop out the function, because it decrypts the stage 2 flag 
while you enter the codes. 
At the very last code, it will not show you the code you have to calculate, so you have to patch the function in order to see the last code (Did I do this in the final version?? I feel like I might have left it out).
Alternatively, you can dynamically debug your way through the function. Just be cautious of the anti-debugging in place.
The program will act as its own tracer upon execution and terminate if it fails to do so. This means that you cannot start the program with gdb, 
and you also cant attach to the running program.
The section headers in the binary are bogus, causing some disassemblers to crash while analyzing the file (this might be fixed in newer versions, it used to work a few years ago).

There is no reference to ptrace anywhere, because I have unwrapped calls to functions such as *ptrace*, *alarm* 
and instead used raw syscalls. Your favorite disassembly tool might be smart enough to re-insert the references to the functions. 

If you patch the stage 2 function correctly, your flag with be decrypted and printed after 50 codes. 

This stage can also be completed entirely through static analysis (which is probably the easiest tbh). Extract the flag (easy to find, you can see 
where it tries to print it), and find the sequence it is being xor'd with. 

In ghidra, the 'reward' print and actual xor'ing are right next to each other in the decompilation window, so it should be easy to extract. 

## Stage 3

Stage 3 is a bit more difficult, and I hope no one will solve this. I have inlined a function throughout this stage that will do a slight
*integrity check* to see if a key from stage 2 exists in memory. If not, terminate and/or quietly null the flag buffer.

In stage 3 you have to cut the right wires. However, the random generator is statically seeded with `0xdeadbabe`, so you can predict the sequence. 
It will slowly decrypt a huge buffer which contains the final step in the challenge. 

If you wanna get debugging working for dynamic analysis, nop the function in the .init_array that blocks debugging. 

You finally get an mmap'ed area and the pointer to the begging is printed. In this new map, you get what looks like an elf file. 
I suggest dumping the buffer to disk. Its a movfuscated binary that prints the final flag. You need to extract the binary and run it to get the final flag. The binary contains a `strcmp` call that never succeeds. You will need to manually bypass it in GDB or patch it. Good luck!

Look into the movfuscator project if you are interested, the author is a super cool guy and his projects are absolutely amazing! (movfuscator, sandsifter etc.). 
