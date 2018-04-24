import sys
import binascii

########Currently Hardcoded, change to whatever##########
encode = False
bitMode = False
offset = 1024
interval = 1
wrapper = ""
hidden = ""


arguments = sys.argv[1:]
for args in arguments:
    if "-b" in args:
        bitMode = True
    if "-s" in args:
        encode = True
    if "-o" in args:
        offset = int(args[2:] )     
    if "-i" in args:
        interval = int(args[2:])
    if "-w" in args:
        wrapper = args[2:]
    if "-h" in args:
        hidden = args[2:]

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
    

    #initalize j, j is used to walk through the entire list of hidden binary values
    j = 0
    for i in range(len(hidden_bin)):
        if (bitMode):
            #Use a for loop, loops through the entire byte of hidden data
            for k in range(0,8):

                #Set value at offset, AND wiht 11111110, and convert back to binary, then back to string
                storage_bin[offset] = str(bin(int(storage_bin[offset],2) & int("11111110",2))[2:].zfill(8))


                #AND the value inside of hidden list, shift to the left to get the smallest bit, then OR the value with storage.
                #After that, convert back to string
                storage_bin[offset] = str(bin(int(storage_bin[offset],2) | ((int(hidden_bin[j],2) & int("10000000")) >> 7))[2:].zfill(8))

                #Change the value of hidden list to be shifted to the right, to continue in the for loop
                hidden_bin[j] = str(bin(int(hidden_bin[j],2) << 1)[2:].zfill(8))

                #Offset increases, to navigate to next interval. This value can be changed
                offset+=1
            #increment j, to continue down the list of hidden binary values
            j+=1
            
        else:
            #Byte method, replace the entire byte in array with the byte of hidden list
            storage_bin[offset] = hidden_bin[i]

            #Add to the interval to continue down the list
            offset+=interval
    
    output(storage_bin)
else:
    #Convert the file into array of characters 
    storage_bytes = fileIntoArray(wrapper)

    #convert the array of characters into binary
    storage_bin = chrToBin(storage_bytes)

    newFile = []
    senLength = len(sentinel_string)
    #While the string value of the sentinel string is not at the very end of the array, keep looping.
    #Eventually the sentinel will be added, will be noticed, and then promptly removed.
    while sentinel_string not in ''.join(newFile[-senLength:]):
        if (bitMode):

            #Instantiates a new string that is null
            newString = ""
            for bit in range(0,8):
                #For the length of the hidden byte, grab the last digit in the index, and add it to the string
                newString += storage_bin[offset][7]
                #Can be changed, but increment down the offset to get the next least significant bit
                offset+=1
            #Once the bit is full, add it to the newFile string
            newFile.append(newString)
            
        else:
            #Grab the entire byte in storage bin, and add it to the newFile list
            newFile.append(storage_bin[offset])
            #Increase by the interval passed in to reach the next value stored.
            offset+=interval
    #Remove the sentinel from the end of the array
    newFile = newFile[:-7]
    #Output the current Array containing the newFile
    output(newFile)


