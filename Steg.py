import sys
import binascii

########Currently Hardcoded, change to whatever##########
ENCODE = "unset"
BIT = "unset"
OFFSET = 1024
INTERVAL = 1
WRAPPER = "unset"
HIDDEN = "unset"
ENDIAN = False


arguments = sys.argv[1:]
for args in arguments:

	if "-u" in args[0:2]:
			sys.stdout.write("Usage: python Steg.py -b -s -o1024 -i2 -wfile -hfile\n")
			sys.exit()

	if "-b" in args[0:2]:
		BIT = True
	if "-B" in args[0:2]:
		BIT = False

	if "-s" in args[0:2]:
		ENCODE = True
	if "-r" in args[0:2]:
		ENCODE = False

	if "-e" in args[0:2]:
		ENDIAN = True

	if "-o" in args[0:2]:
		OFFSET = int(args[2:] )	 
	if "-i" in args[0:2]:
		INTERVAL = int(args[2:])

	if "-w" in args[0:2]:
		WRAPPER = args[2:]
	if "-h" in args[0:2]:
		HIDDEN = args[2:]

#Can be hardcoded, as the sentinel will not change
sentinel_bytes = [chr(0x0),chr(0xFF),chr(0x0),chr(0x0),chr(0xFF),chr(0x0)]
sentinel_string = '000000001111111100000000000000001111111100000000'
sentinel_binary = ["00000000", "11111111", "00000000", "00000000", "11111111", "00000000"]

if (WRAPPER == "unset"):
	sys.stdout.write("Incorrect usage use -u to show corect usage")
	sys.exit("You must specify a wrapper file (-w<val>)")
if (ENCODE == "unset"):
	sys.stdout.write("Incorrect usage use -u to show corect usage")
	sys.exit("You must specify -s (store) or -r (retrieve)")


def fileToBinary(fileName):
	binaryArray = []
	f = open(fileName, "rb")
	contents = f.read()
	f.close

	binaryArray = bytearray(contents)
		
	return binaryArray

#Takes in an array, and iterates through the entire array to produce a new image.
def output(outputArr):
	for byte in outputArr:
		sys.stdout.write(byte)
		#sys.stdout.write(chr(int(byte,2)))
	
#Two different flows of program, one if encoding and one if we are decoding
if(ENCODE):
	
	# Get binary array from the file to hide
	hidden_bin2 = fileToBinary(HIDDEN)
	# Append the sentinel to the binary array
	for item in sentinel_binary:
			hidden_bin2.append(item)

	storage_bin = fileToBinary(WRAPPER)
	

	#initalize j, j is used to walk through the entire list of hidden binary values
	j = 0
	for i in range(len(hidden_bin)):
		if (BIT):
			#Use a for loop, loops through the entire byte of hidden data
			for k in range(0,8):

				#Set value at OFFSET, AND with 11111110, and convert back to binary, then back to string
				storage_bin[OFFSET] = str(bin(int(storage_bin[OFFSET],2) & int("11111110",2))[2:].zfill(8))


				#AND the value inside of hidden list, shift to the left to get the smallest bit, then OR the value with storage.
				#After that, convert back to string
				storage_bin[OFFSET] = str(bin(int(storage_bin[OFFSET],2) | ((int(hidden_bin[j],2) & int("10000000")) >> 7))[2:].zfill(8))

				#Change the value of hidden list to be shifted to the right, to continue in the for loop
				hidden_bin[j] = str(bin(int(hidden_bin[j],2) << 1)[2:].zfill(8))

				#OFFSET increases, to navigate to next INTERVAL. This value can be changed
				OFFSET+=1
			#increment j, to continue down the list of hidden binary values
			j+=1
			
		else:
			#Byte method, replace the entire byte in array with the byte of hidden list
			storage_bin[OFFSET] = hidden_bin[i]

			#Add to the INTERVAL to continue down the list
			OFFSET+=INTERVAL
	
	output(storage_bin)

else: # We are decoding

	#sys.stdout.write(''.join(sentinel_bytes))
	#exit()

	storage_bin = fileToBinary(WRAPPER)

	newFile = []
	senLength = len(sentinel_bytes)
	#While the string value of the sentinel string is not at the very end of the array, keep looping.
	#Eventually the sentinel will be added, will be noticed, and then promptly removed.
	while sentinel_bytes != newFile[-senLength:]:
		if (BIT):



			#Instantiates a new string that is null
			newString = ""
			for bit in range(0,8):
				if (ENDIAN):
					
					# Get the last bit and add it to the beginning of our 'byte'
					newString = str(1 & storage_bin[OFFSET]) + newString
				else:
					#sys.stdout.write(str(storage_bin[OFFSET])+"\n")
					#exit()
					
					# Get the last bit and add it to the end of our 'byte'
					newString += str(1 & storage_bin[OFFSET])


					#For the length of the hidden byte, grab the last digit in the index, and add it to the string
					#Can be changed, but increment down the OFFSET to get the next least significant bit
					OFFSET+=INTERVAL

			#Once the bit is full, add it to the newFile string
			newFile.append(chr(int(newString,2)))
			
		else:

			#output(newFile[-senLength:])
			#sys.stdout.write('\n')
			#exit()

			byte = chr(storage_bin[OFFSET])

			

			#Grab the entire byte in storage bin, and add it to the newFile list
			newFile.append(byte)
			#Increase by the INTERVAL passed in to reach the next value stored.
			OFFSET+=INTERVAL
	#Remove the sentinel from the end of the array
	newFile = newFile[:-7]
	#Output the current Array containing the newFile
	output(newFile)


