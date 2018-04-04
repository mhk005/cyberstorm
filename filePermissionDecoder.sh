#!/bin/bash



#-------------------------------------------------------------------------------
# Written By: Mark Harms                                           TEAM PATIENCE
#-------------------------------------------------------------------------------
# USAGE: bash filePermissionDecoder.sh -[se][tf][0-9] [directoryPath] [ftpServer] [USER] [PASS]
# Examples:
#		bash filePermissionDecoder.sh -et8 ~/Desktop/permissionMsg
#		bash filePermissionDecoder.sh -st7 ~/Desktop/permissionMsg2
#		bash filePermissionDecoder.sh ~/Dektop/permissionMsg
#		bash filePermissionDecoder.sh messagePath jeangourd.com anonymous ""
#-------------------------------------------------------------------------------
# DESCRIPTION: 
#   This program takes a directory path and parses file permissions
#   of files contained within the directory, translating them into an
#   ASCII message, how decoding happens is based on 3 flag sets:
#		
#     Decode Override: -e = 8-bit ASCII 	-s = 7-bit ASCII
#	DEFAULT: Both are printed
#	 	
#     Ignored bits: -[0-9] This sets how many leading bits of each
#	line are ignored 	
#	DEFAULT VALUE: 0
#
#     Skip Flag: -t = true, ignored bits are trated as a flag to skip the line
#		        of input
#		 -f = false, ignored bits are just skipped
#       DEFAULT VALUE: False
#-------------------------------------------------------------------------------




################################################################################
# sevenBitDecoder()
#-------------------------------------------------------------------------------
# INPUTS	 |	 DESCRIPTION
# $input         | String of 0's and 1's to be translated to ASCII
#-------------------------------------------------------------------------------
# OUTPUTS	 |
# ECHO           | ASCII results are echoed to Stdout
################################################################################
sevenBitDecoder () 
{
	sevenTest="" # Setup an empty string 

	for (( i=0; i<${#input}; i+=7 )); # Loop through the binary 7 bits at a time
	do
        	sevenTest+="0" # Pad our 7-bit binary to 'make' it 8-bit
        	sevenTest+=${input:$i:7} # Get the following 7 bits                     
	done
	echo $sevenTest | perl -ple '$_=pack"B*",$_' # Translate our binary to ASCII
}



################################################################################
# eightBitDecoder()
#-------------------------------------------------------------------------------
# INPUTS	 |	 DESCRIPTION
# $input         | String of 0's and 1's to be translated to ASCII
#-------------------------------------------------------------------------------
# OUTPUTS	 |
# ECHO           | ASCII results are echoed to Stdout
################################################################################
eightBitDecoder () 
{
	echo $input | perl -lpe '$_=pack"B*",$_' # Translate our binary to ASCII
}



################################################################################
# permissionDecoder()
#-------------------------------------------------------------------------------
# INPUTS	 |	 DESCRIPTION
# $pInput	 | List of permissions to decode
# $skipFlag	 | Flag indicating whether or not ignored bits flag to skip the entire line
# $ignoreCount   | Number of bits to skip (0-9) when decoding
#-------------------------------------------------------------------------------
# OUTPUTS	 |
# $bitHolder     | String of 0's and 1's to be translated to ASCII
################################################################################
permissionDecoder ()
{
	bitHolder=""
	pLength=${#pInput}
	for (( i=0; i<$pLength; i+=11 )) # Get one 'line' at a time
	do	# Check if ignored bits indicate skipping a line of input
		if [ "$skipFlag" = "true" ]
		then
			weSkip="false" # We assume no bits are set to skip
			for (( j=0; j<$ignoreCount; j++ ));
			do
				# If we find a 'true' bit
				if [ ${pInput:$((i+j)):1} != "-" ]
				then
					weSkip="true" # Set a flag to skip
					break # Break out of loop, we know we skip
				fi
			done
			# If our flag is set, we skip the rest of the loop
			if [ "$weSkip" = "true" ]
			then
				continue
			fi
		fi
		
		# Iterate through non-skipped bits
		for (( k=$ignoreCount; k<10; k++ ))
		do
			value=${pInput:$((i+k)):1} # Get the value of our bit
			
			# If "-" we add a 0 to our bitHolder
			if [ "$value" = "-" ]
			then
				bitHolder+="0"
			# Otherwise, check for a valid non "-" character
			# if it is valid, add a 1 to our bitHolder
			elif [ "$value" = "d" ] || [ "$value" = "l" ] || [ "$value" = "r" ] || [ "$value" = "w" ] || [ "$value" = "x" ]
			then
				bitHolder+="1"
			else # Otherwise, we have some invalid input
				# Tell the user about the error and exit
				>&2 echo "Invalid input detected"
				exit 1
			fi
		done
	done
}



# Default script values
ignoreCount=0
skipFlag="false"
USER="anonymous"
PASS=""



# Get the passed in options and set the associated flag values
while getopts ":setf0123456789" option;
do
	pSet="true"
        case ${option}
        in
		# Default is decoding in both 7- and 8-bit
                s) decodeOverride="seven" ;; # Override to decode only 7-bit ASCII
                e) decodeOverride="eight" ;; # Override to decode only 8-bit ASCII
		
		# Set whether ignored bits are treated as a flag
		# to skip the line of input    Default Value: False

		t) skipFlag="true" ;;
		f) skipFlag="false" ;;

		# Set the number of ignored bits
		# Default Value: 0
		0) ignoreCount=0 ;;
		1) ignoreCount=1 ;;
		2) ignoreCount=2 ;;
		3) ignoreCount=3 ;;
		4) ignoreCount=4 ;;
		5) ignoreCount=5 ;;
		6) ignoreCount=6 ;;
		7) ignoreCount=7 ;;
		8) ignoreCount=8 ;;
		9) ignoreCount=9 ;;
         esac
done


# Get passed in variables
# If we pass in flags we need to offset vars by 1
if [ "$pSet" = "true" ] 
then	
	# Directory to read from
	dirPath="$2"

	# -n tests if the variable is set

	# if we pass in a host set it and set a flag that we are using ftp
	if [ -n "$3" ] 
	then
		HOST="$3"
		ftpConnect="true"
	fi
	if [ -n "$4" ] # user passed in a username
	then
		USER="$4"
	fi
	if [ -n "$5" ] # user passed in a password
	then
		PASS="$5"
	fi
else
	dirPath="$1"
	
	if [ -n "$2" ]
	then
		HOST="$2"
		ftpConnect="true"
	fi
	if [ -n "$3" ]
	then
		USER="$3"
	fi
	if [ -n "$4" ]
	then
		PASS="$4"
	fi
fi


# Body of the script

if [ "$ftpConnect" = "true" ]
then
	touch filepermissionout.txt
	chmod 666 filepermissionout.txt

	ftp -n $HOST > /dev/null <<END_SCRIPT
	quote USER $USER
	quote PASS $PASS
	cd $dirPath
	ls -l filepermissionout.txt
	y
	exit
END_SCRIPT
	# pInput is passed to permissionDecoder
	pInput="$(grep -o [dl-][r-][w-][x-][r-][w-][x-][r-][w-][x-] < filepermissionout.txt)"
	rm filepermissionout.txt

else
	# pInput is passed to permissionDecoder
	pInput="$(ls -l $dirPath | grep -o [dl-][r-][w-][x-][r-][w-][x-][r-][w-][x-])"
fi

permissionDecoder


# input is passed to seven/eightBitDecoder
input=$bitHolder
if [ "$decodeOverride" = "seven" ];
then
	sevenBitDecoder
elif [ "$decodeOverride" = "eight" ];
then
	eightBitDecoder
else
	sevenBitDecoder
	eightBitDecoder
fi
echo

exit 0
