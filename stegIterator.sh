#!/bin/bash

mkdir -p _OUTPUTS

COLOR='\033[1;36m'
NC='\033[0m'

while getopts ":bB" option;
do 
		case ${option}
		in
			b) bString="-b" ;;
			B) bString="-B" ;;

		esac
done

if [ -z $3 ]
then
	tnum=1
else
	tnum=$3
fi

if [ -z $4 ]
then
	num=1
else
	num=$4
fi

count=0

for (( j=$tnum; j<513; j*=2 ));
do
	for (( i=$num; i<4097; i*=2 ));
	do
		echo
		echo "Trying Offset:$i Interval:$j"
		#echo "python Steg.py $bString -r -o$i -i$j -w$2"
		$(python Steg.py $bString -r -o$i -i$j -w$2 > ./_OUTPUTS/"$i"-"$j" 2>/dev/null) && echo -e "${COLOR}Success${NC}" && count=$((count+1)) || rm ./_OUTPUTS/"$i"-"$j"
		
		
		#echo "Output is :$output"
		#echo "stegOut_0$(i)_$j"

	done
done

echo -e "\n${COLOR}$count successful${NC}" 
