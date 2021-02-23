.PHONY: clean release default

CC=gcc
CFLAGS=-Wall -pedantic -Wextra
DEPS= 
LIBS=-lseccomp

default: debug

debug: CFLAGS += -DDEBUG -D SKIP_PTRACE -g
debug: seccomp2abyss

release: CFLAGS += -O3
release: seccomp2abyss
	 @objcopy --strip-all $^
	 @objcopy --remove-section .note.ABI-tag $<
	 @objcopy --remove-section .gnu.version $<
	 @objcopy --remove-section .gnu.hash $<

seccomp2abyss:
	$(CC) -o $@ main.c $(CFLAGS) $(LIBS)
clean:
	rm -f *.o *~ seccomp2abyss
