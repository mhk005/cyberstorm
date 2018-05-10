#!/bin/bash
# This is a bash script that 'detects' whether binary input is 7- or 8-bit
# and then outputs the corresponding ASCII to the binary input.
# proper execution of the program is [ bash binaryDecoder.sh < input.txt ]


# Get input from stdin
input=$(cat)

# Get the length of the input
length=${#input}

# Test for 7-bit ASCII
	sevenTest="" # Setup an empty string 

	for (( i=0; i<${#input}; i+=7 )); do # Loop through the binary 7 bits at a time
	
		sevenTest+="0" # Pad our 7-bit binary to 'make' it 8-bit
		sevenTest+=${input:$i:7} # Get the following 7 bits			
	done
	echo $sevenTest | perl -ple '$_=pack"B*",$_' # Translate our binary to ASCII

# Test for 8-bit ASCII
	echo $input | perl -lpe '$_=pack"B*",$_' # Translate our binary to ASCII

# Test for case of bad input
if [ $((length % 7)) != 0 ] && [ $((length % 8)) != 0 ]
then
	echo "The input is neither 7-bit nor 8-bit and thus could not be decoded"
fi


exit 0
