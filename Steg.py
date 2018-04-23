import sys
import binascii

########Currently Hardcoded, change to whatever##########
encode = False
offset = 1024
interval = 8
wrapper = "stegged-byte.bmp"
hidden = "Sample.jpeg"

#Can be hardcoded, as the sentinel will not change
sentinel_bytes = [chr(0x0),chr(0xFF),chr(0x0),chr(0x0),chr(0xFF),chr(0x0)]
sentinel_string = '000000001111111100000000000000001111111100000000'

#Takes in a filename string as imput, opens that filename, and stores the contents into an array and returns it
def fileIntoArray(fileName):
    byteArray = []
    with open(fileName, "rb") as f:
	byte = f.read(1)
	while byte != "":
		byteArray.append(byte)
		byte = f.read(1)
    return byteArray
#takes an array of characters, and converts this array into binary values for each 
def chrToBin(chrBytes):
    chrBin = []
    for byte in chrBytes:
        #Found this on stack overflow. Removes the leading 0b for binary word, as well as forces the value to have length of 8.
        #A standard Bin() function does not work, because it removes leading 0's, and is annoying to mess with.
        chrBin.append((''.join('{0:08b}'.format(x, 'b') for x in bytearray(byte))))
        
    return chrBin
#Takes in an array, and iterates through the entire array to produce a new image.
def output(outputArr):
    for byte in outputArr:              
	sys.stdout.write(chr(int(byte,2)))
	
#Two different flows of program, one if encoding and one if we are decoding
if(encode):
    #Convert the file into array of characters   
    hidden_bytes = fileIntoArray(hidden)
    
    #Add the sentinal to the end of the hidden picture you are encoding
    hidden_bytes.extend(sentinel_bytes)
    
    #convert the array of characters into binary 
    hidden_bin = chrToBin(hidden_bytes)
	
    #Convert the file into array of characters
    storage_bytes = fileIntoArray(wrapper)
    
    #convert the array of characters into binary	
    storage_bin = chrToBin(storage_bytes)
	
	
    for i in range(len(hidden_bin)):
	'''

        INSERT BIT VERSION HERE, EITHER AS FUNCTION, OR INSIDE FOR LOOP
        





        '''
	storage_bin[offset] = hidden_bin[i]
	offset+=interval
	
    output(storage_bin)
else:
    #Convert the file into array of characters 
    storage_bytes = fileIntoArray(wrapper)

    #convert the array of characters into binary
    storage_bin = chrToBin(storage_bytes)

    newFile = []
    i = 0
    senLength = len(sentinel_string)
    #While the string value of the sentinel string is not at the very end of the array, keep looping.
    #Eventually the sentinel will be added, will be noticed, and then promptly removed.
    while sentinel_string not in ''.join(newFile[-senLength:]):

        '''

        INSERT BIT VERSION HERE, EITHER AS FUNCTION, OR INSIDE FOR LOOP
        





        '''
        newFile.append(storage_bin[offset])
        offset+=interval
        i = i+1
    #Remove the sentinel from the end of the array
    newFile = newFile[:-7]
    #Output the current Array containing the newFile
    output(newFile)
