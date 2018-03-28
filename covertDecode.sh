#!/bin/bash

sevenDecode () 
{
	sevenTest="" # Setup an empty string 

	for (( i=0; i<${#input}; i+=7 )); # Loop through the binary 7 bits at a time
	do
        	sevenTest+="0" # Pad our 7-bit binary to 'make' it 8-bit
        	sevenTest+=${input:$i:7} # Get the following 7 bits                     
	done
	echo $sevenTest | perl -ple '$_=pack"B*",$_' # Translate our binary to ASCII
}


eightDecode () 
{
	echo $input | perl -lpe '$_=pack"B*",$_' # Translate our binary to ASCII
}


# Get the option the user selected
while getopts ":se" option;
do
        case ${option}
        in
                s) sevenOverride="true"
                        ;;
                e) eightOverride="true"
                        ;;
        esac
done

if [ "$sevenOverride" = "true" ] && [ "$eightOverride" = "true" ];
then
        echo "You may only select either -s 7-bit or -e 8-bit."
	echo "If you wish both to be output then omit the option"
        exit 1
fi


######################## NOTE: For the assignment I suggest to run in -s mode since
######################## both outputs are correct with the 7-bit interpretation.

touch sevenOut.txt
touch tenOut.txt
chmod 666 sevenOut.txt
chmod 666 tenOut.txt

HOST='jeangourd.com'
USER='anonymous'
PASSWD=''

ftp -n $HOST > /dev/null <<END_SCRIPT
quote USER $USER
quote PASS $PASSWD
cd 7
ls -Rl sevenOut.txt
y
cd ../10
ls -Rl tenOut.txt
y
exit
END_SCRIPT


sevenList="$(grep -o [dl-][r-][w-][x-][r-][w-][x-][r-][w-][x-] < sevenOut.txt)"
tenList="$(grep -o [dl-][r-][w-][x-][r-][w-][x-][r-][w-][x-] < tenOut.txt)"

rm sevenOut.txt
rm tenOut.txt


sevenBit=""
sevenLength=${#sevenList}
for (( i=0; i<$sevenLength; i+=11 ));
do
	case1=${sevenList:$i:1}
	case2=${sevenList:$((i+1)):1}
	case3=${sevenList:$((i+2)):1}
	
	if [ "$case1" = "-" ] && [ "$case2" = "-" ] && [ "$case3" = "-" ]
	then
		for (( j=3; $j<10; j++ ));
		do
			value=${sevenList:$((i+j)):1}
        
			if [ "$value" = "-" ]
       			then
                		sevenBit+="0"
        		elif [ "$value" = "d" ] || [ "$value" = "l" ] || [ "$value" = "r" ] || [ "$value" = "w" ] || [ "$value" = "x" ]
        		then
                		sevenBit+="1"
        		fi
		done
	fi
done


tenBit=""
tenLength=${#tenList}
for (( i=0; i<$tenLength; i++ )); 
do
	value=${tenList:$i:1}
	
	if [ "$value" = "-" ]
	then
		tenBit+="0"
	elif [ "$value" = "d" ] || [ "$value" = "l" ] || [ "$value" = "r" ] || [ "$value" = "w" ] || [ "$value" = "x" ]
	then
		tenBit+="1"
	fi
done


input="$sevenBit"
length=${#input}
if [ "$sevenOverride" = "true" ];
then
	sevenDecode
elif [ "$eightOverride" = "true" ];
then
	eightDecode
else
	sevenDecode
	eightDecode
fi
echo


input="$tenBit"
length=${#input}
if [ "$sevenOverride" = "true" ];
then
        sevenDecode
elif [ "$eightOverride" = "true" ];
then
        eightDecode
else
        sevenDecode
        eightDecode
fi


exit 0

