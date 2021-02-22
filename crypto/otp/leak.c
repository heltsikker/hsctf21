#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

int main(void) {
	size_t key_len = 32;

	uint8_t *key = calloc(1, key_len);
	for (int i = 0; i < key_len; i++) {
	       	key[i] = rand();
	}
	
	printf("Key: ");
	for (int i = 0; i < key_len; i++) {
		// prints the data as human-readable hex characters
		printf("%02hhX", key[i]);
	}
	printf("\n");

	return 0;
}
