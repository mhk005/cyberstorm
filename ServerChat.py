import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 31339
s.bind(("",port))

s.listen(0)

c,addr = s.accept()
from binascii import hexlify
covert = "secret" + "EOF"
covert_bin = ""
for i in covert:
# convert each character to a full byte
# hexlify converts ASCII to hex
# int converts the hex to a decimal integer
# bin provides its binary representation (with a 0b
# prefix that must be removed)
# that's the [2:] (return the string from the third
# character on)
# zfill left-pads the bit string with 0s to ensure a
# full byte
    covert_bin += bin(int(hexlify(i), 16))[2:].zfill(8)
print(covert_bin)
import time
ZERO = 0.025
ONE = 0.1
msg = "Some message... A very Special Message that only team Patience Can see because its being ran on local host.\n"
n = 0
for i in msg:
    c.send(i)
    if (covert_bin[n] == "0"):
        time.sleep(ZERO)
    else:
        time.sleep(ONE)
    n = (n + 1) % len(covert_bin)
c.send("EOF")
c.close()
