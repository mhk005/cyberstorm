import socket
import sys
from time import time
from binascii import unhexlify

ip = "jeangourd.com"
port = 31337

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect((ip,port))
#overt = ''
covert_bin = ""
data = s.recv(4096)
while(data.rstrip("\n") != "EOF"):
    sys.stdout.write(data)        
    sys.stdout.flush()
 #   covert_bin = ""
    t0 = time()
    data = s.recv(4096)
    t1 = time() 
    delta = round(t1-t0,3)
 #   print(delta)
    if (delta >= 0.085):
        covert_bin += "1"
    else:
        covert_bin += "0"
   # print covert_bin
    i = 0
    covert = ""
    while (i< len(covert_bin)):
        b = covert_bin[i:i+8]
        n = int("0b{}".format(b),2)
        try:
            covert += unhexlify("{0:x}".format(n))
        except TypeError:
            covert += "?"

        i += 8
s.close()
print(covert)
