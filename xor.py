#############################################
#Name: XOR Cipher
#Author: Team Patience
#Description: Takes in standard input, bit by bit, and XOR these bits to a file in
#   in the same directory called key!
#############################################



import sys

cyphertext = ''

for byte in sys.stdin:
    for bit in byte:
        cyphertext+=bit

key = ""
with open("key","rb") as file:
    text = file.read(1)
    while(len(text) != 0):
        key +=text
        text = file.read(1)

if len(key) != len(cyphertext):
    print("ERROR! Key Size and CypherText size must be the same!")
    print("The Length of Key Size is "+ str(len(key))+", while the length of the cyphertext is "+ str(len(cyphertext)))
else:
    for i in range(len(key)):
        sys.stdout.write(str(chr(ord(key[i]) ^ ord(cyphertext[i]))))
        
