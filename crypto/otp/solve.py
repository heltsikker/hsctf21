from binascii import unhexlify

# hex data from task description
encrypted = unhexlify("2F952A2717841E844C92EAF49B95BC162E8C13A77F8782FE293441176CECBDFB09A236153E8D15BC4CBFDCCE918F9E")

# hex data from leak.c which prints the key variable instead of encrypted variable
key = unhexlify("67C6697351FF4AEC29CDBAABF2FBE3467CC254F81BE8E78D765A2E63339FC99A")

# basic xor of key and encrypted data to get flag
flag = "".join([chr(ord(x) ^ ord(y)) for x,y in zip(encrypted, key*10)])

print("Flag: " + flag)
