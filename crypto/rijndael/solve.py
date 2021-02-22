import sys

if len(sys.argv) != 2:
    print("Usage: python3 {} CIPHERTEXT".format(sys.argv[0]))
    sys.exit(1)

encrypted = sys.argv[1]

auth = "name=admin&server=cyberbarricade&auth=0"

byte_to_flip = auth.index("0") # we want to flip auth=0 to auth=1
byte_to_flip -= 16 # flip previous block
byte_to_flip *= 2 # the encrypted text uses 2 hex chars per byte

flip_value = ord("0") ^ ord("1") # XOR key to change "0" to "1"

byte = encrypted[byte_to_flip:byte_to_flip+2] # fetch the 2 chars we want to change
byte = int(byte, 16) # convert it to a decimal value from 0 to 255
byte ^= flip_value # XOR with key
byte = hex(byte)[2:] # convert to hex and remove the leading "0x" characters

data = encrypted[:byte_to_flip] + byte + encrypted[byte_to_flip+2:] # generate a new string with our changed byte

print(data)
