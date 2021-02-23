#include <fcntl.h>
#include <seccomp.h>
#include <signal.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/prctl.h>
#include <unistd.h>


#define READ_SIZ (61)

void (* sc)();

bool preprocess(unsigned char * p, ssize_t b) {
  for (ssize_t i = 0; i < b; i++) {
    if ((uint8_t)p[i] == 0x01 || (uint8_t)p[i] == 0x00 || (uint8_t)p[i] == 0x02)
      return false;
  }
  return true;
}

int main() {

  int bytes_read = 0;


  unsigned char buf[READ_SIZ];

  setvbuf(stdout, NULL, _IONBF, 0);
  
  printf("~~ FOOL! GIVE ME YOUR BEST ~~\n");

  sc = mmap(NULL, READ_SIZ, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANON, -1, 0);
  
  scmp_filter_ctx ctx;
  ctx = seccomp_init(SCMP_ACT_KILL);

  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(rt_sigreturn), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);

  if (0 < (bytes_read = read(0, buf, READ_SIZ))) {
    if (!preprocess(&buf, bytes_read)) {
      printf("~~THAT'S NOT ALLOWED~~\n");
      exit(0);
    }
    memcpy(sc, &buf, bytes_read);
    seccomp_load(ctx);
    sc();
  }

  return 0;
}
