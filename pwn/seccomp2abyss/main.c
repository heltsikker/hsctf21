#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>

#include <sys/mman.h>
#include <sys/prctl.h>
#include <seccomp.h>

#define PG_SIZ (4096)

void (* sc)();

/* char shellcode[] = "\xeb\x35\x5f\x48\x31\xc0\x04\x02\x48\x31\xf6\x0f\x05\x48\x89\xc7\x48\x8d\x34\x24\x48\x31\xd2\x66\xba\xff\x0f\x48\x31\xc0\x0f\x05\x48\x31\xff\x40\xb7\x01\x48\x89\xc2\x48\x31\xc0\xb0\x01\x0f\x05\x48\x31\xc0\xb0\x3c\x0f\x05\xe8\xc6\xff\xff\xff\x66\x6c\x61\x67\x2e\x74\x78\x74"; */

int main() {

  setvbuf(stdout, NULL, _IONBF, 0);
  
  printf("~~ FEED ME AND SUCCOMB TO THE ABYSS ~~\n");

  
  sc = mmap(NULL, PG_SIZ, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANON, -1, 0);

  scmp_filter_ctx ctx;
  ctx = seccomp_init(SCMP_ACT_KILL);

  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(rt_sigreturn), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);

  seccomp_load(ctx);
  
  if (0 < read(0, sc, PG_SIZ)) {
    sc();
  }

  return 0;
}
