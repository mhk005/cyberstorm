#############################################
#Name: XOR Cipher
#Author: Team Patience
#Description: Takes in standard input, bit by bit, and XOR these bits to a file in
#   in the same directory called key!
###############PYTHON 2##############################
#############################################



import sys
#Initialize an empty string to build upon later
cyphertext = ''

#Stdin takes input by lines, so first grab every line
for line in sys.stdin:
    #For every bit in each line, add it to the cyphertext string intialized earlier
    for bit in line:
        cyphertext+=bit
#Initialize an empty string to build upon later
key = ""
#Open the file named "key" in current directory
with open("key","rb") as file:
    #Read the first bit in the file
    text = file.read(1)
    #Continue reading until you get a null character
    while(len(text) != 0):
        #Build string with bits
        key +=text
        #read next bit
        text = file.read(1)
#The Key and the File passed in have to be the same size, otherwise output an error
if len(key) != len(cyphertext):
    print("ERROR! Key Size and CypherText size must be the same!")
    print("The Length of Key Size is "+ str(len(key))+", while the length of the cyphertext is "+ str(len(cyphertext)))
else:
    #Loop through the entire list in key
    for i in range(len(key)):
        #Write the bit, do the XOR operand for each individual bit in each list, have to translate from ord() function to
        #get correct value. Change the XOR'd bit back into a character. Make sure it's still a string!!
        sys.stdout.write(str(chr(ord(key[i]) ^ ord(cyphertext[i]))))
        
