from pwn import *

r = remote("127.0.0.1", 8001)

r.recvuntil("x=")
x = int(r.recvuntil(",")[:-1])

r.recvuntil("y=")
y = int(r.recvuntil(")")[:-1])

p = 39402006196394479212279040100143613805079739270465446667948293404245721771496870329047266088258938001861606973112319
o = 39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942643
a = -3
b = 0xB3312FA7E23EE7E4988E056BE3F82D19181D9C6EFE8141120314088F5013875AC656398D8A2ED19D2A85C8EDD3EC2AEF


r.recv()
r.sendline(', '.join([str(i) for i in [p, o, a, b, x, y, 1]]))

print(r.recv())
