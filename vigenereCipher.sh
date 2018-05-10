#!/bin/bash
# Coded by Mark Harms (3/27/2018)


# Declare some arrays to help us with our cipher functionality
declare -A lowers
lowers=( ["a"]=0 ["b"]=1 ["c"]=2 ["d"]=3 ["e"]=4 ["f"]=5 ["g"]=6 ["h"]=7 ["i"]=8 ["j"]=9 ["k"]=10 ["l"]=11 ["m"]=12 ["n"]=13 ["o"]=14 ["p"]=15 ["q"]=16 ["r"]=17 ["s"]=18 ["t"]=19 ["u"]=20 ["v"]=21 ["w"]=22 ["x"]=23 ["y"]=24 ["z"]=25 )
lowerKeys=( "a" "b" "c" "d" "e" "f" "g" "h" "i" "j" "k" "l" "m" "n" "o" "p" "q" "r" "s" "t" "u" "v" "w" "x" "y" "z" )

declare -A uppers
uppers=( ["A"]=0 ["B"]=1 ["C"]=2 ["D"]=3 ["E"]=4 ["F"]=5 ["G"]=6 ["H"]=7 ["I"]=8 ["J"]=9 ["K"]=10 ["L"]=11 ["M"]=12 ["N"]=13 ["O"]=14 ["P"]=15 ["Q"]=16 ["R"]=17 ["S"]=18 ["T"]=19 ["U"]=20 ["V"]=21 ["W"]=22 ["X"]=23 ["Y"]=24 ["Z"]=25 )
upperKeys=( "A" "B" "C" "D" "E" "F" "G" "H" "I" "J" "K" "L" "M" "N" "O" "P" "Q" "R" "S" "T" "U" "V" "W" "X" "Y" "Z" )


# Get the option the user selected
while getopts ":ed" option;
do
	case ${option}
	in
		e) encrypt="true"
			;;
		d) decrypt="true"
			;;
		\?) echo "Usage: bash vigenereCipher.sh -[e/d] [key]"
			;;
	esac
done


# Make sure our users entered valid options and a key
if [ "$encrypt" = "true" ] && [ "$decrypt" = "true" ];
then
	echo "You may only select either -e [encrypt] or -d [decrypt], not both."
	echo "Usage: bash vigenereCipher.sh -[e/d] [key]"
	exit 1
fi

if [ -z "$encrypt" ] && [ -z "$decrypt" ];
then
	echo "You must enter either -e [encrypt] or -d [decrypt] as an option."
	echo "Usage: bash vigenereCipher.sh -[e/d] [key]"
	exit 1
fi

if [ -z "$2" ]
then
	echo "You must input a key to use for encryption/decryption."
	echo "Usage: bash vigenereCipher.sh -[e/d] [key]"
	exit 1
fi


# Grab our key from command line, note its length, and declare an array.
securityKey=$2
keyLength=${#securityKey}
declare keyArray


# Loop through the key, storing the integer equivalent of each character in our keyArray
for (( i=0, j=0; i<${#securityKey}; i++, j++ ));
do
	char=${securityKey:$i:1}

	if [ "$char" = " " ];
        then
		keyLength=$((keyLength-1))
		j=$((j-1))
	        continue
        fi

	if [ ${lowers["$char"]+_} ];
	then
		keyArray[$j]=${lowers[$char]}
	elif [ ${uppers["$char"]+_} ];
	then
		keyArray[$j]=${uppers[$char]}
	fi
done


# Read input from stdin one line at a time, we iterate through each line one character
# at a time, encrypting or decrypting it based on which option the user selected
# the encrypted/decrypted text is echoed to stdout
while read -r line;
do
j=0
	for (( i=0; i<${#line}; i++, j++ ))
	do
		j=$(($j % $keyLength)) 

		char=${line:$i:1}
	
		if [ "$char" = " " ];
		then
			echo -n " "
			j=$((j-1))
			continue
		fi

		if [ ${lowers["$char"]+_} ];
		then
			number=${lowers["$char"]}

			if [ "$encrypt" = "true" ];
			then
				number=$(($number + ${keyArray[$j]}))
			elif [ "$decrypt" = "true" ];
			then
				number=$(($number - ${keyArray[$j]} + 26))
			fi

			number=$(($number % 26))
			echo -n ${lowerKeys["$number"]}	
		elif [ ${uppers["$char"]+_} ];
		then
			number=${uppers["$char"]}       

			if [ "$encrypt" = "true" ];
                        then
                                number=$(($number + ${keyArray[$j]}))
                        elif [ "$decrypt" = "true" ];
                        then
                                number=$(($number - ${keyArray[$j]} + 26))
                        fi

                	number=$(($number % 26))
                       	echo -n ${upperKeys["$number"]} 
		else
			j=$((j-1))
			echo -n $char
		fi
	done
	echo ""
done

exit 0
