# OTP Intended Solution
Looking at the attached source file OTP.c we can see that `rand()` is used to generate a 32-byte(256-bit) key, which we should realise is not bruteforceable as it's 2^256 possible keys, when something in a CTF seems impossible it's probably not the intended solution and you have to look for a clever alternative way to solve the problem.

If we research C's `rand()` function we learn that it's a *seeded* pseudo-random number generator and you're supposed to call `srand()` to set the seed before calling `rand()`. Since the application does not call `srand()` to set the seed `rand()` will return the same sequence of numbers every time we run the application and we can leak the "one-time" key  by creating a modified version of the application, for instance [leak.c](leak.c), where we print the `key` variable instead of `encrypted`.

After getting the key it's just a matter of xor'ing the key and the encrypted flag with eachother, but first we have to remember to change the data from it's human-readable form to it's actual byte values, this can for example be done in Python using `binascii.unhexlify()` and you can find my example decryption script in [solve.py](solve.py)

# Alternative Solution
After creating the task we quickly realised that you can call the application a few times and notice that the output of encrypting "asdf" and "asdfghj" starts with the same few characters, revealing that the key is static, knowing how xor is the inverse of itself one can solve the task by simply giving the application the flag from the description in raw bytes using `binascii.unhexlify()` and then using `binascii.unhexlify()` again on the output to instantly get the flag in cleartext.

`(key ^ flag) ^ key = flag`

# Alternative Solution #2
After realising the output of "asdf" and "asdfghj" starts with the same few characters we can leak the key by having a known input like "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" and looking to see when the output starts repeating itself. The challenge can then be solved by xor'ing the output with "a" and then xoring the result with the encrypted key.

`(key ^ 'a') ^ 'a' = key`
`(key ^ flag) ^ key = flag`

# Alternative Solution #3
Who needs a brain when you have strength? After realising that the output is the same for 2 different runs of the same input you can bruteforce the flag one byte at a time by running the program over and over again, comparing the output to the first x bytes of the flag.
