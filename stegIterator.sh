#!/bin/bash

mkdir -p _OUTPUTS

COLOR='\033[1;36m'
NC='\033[0m'

bArray=( "b" "B" )

if [ -z $1 ]
then
	echo "Please input a directory to loop through"
	exit 1
fi

if [ -z $2 ]
then
	num=1
else
	num=$2
fi

if [ -z $3 ]
then
	tnum=1
else
	tnum=$3
fi

thing=1
for k in $1*
do
	count=0
	for bString in "${bArray[@]}"
	do
		for (( j=$tnum; j<513; j*=2 ));
		do
			for (( i=$num; i<4097; i*=2 ));
			do
				mkdir -p _OUTPUTS/"$thing"
				echo
				echo ./_OUTPUTS/"$thing"/-"$bString"-"$i"-"$j"  
				echo "File:$k $bString Offset:$i Interval:$j"
				#echo "python Steg.py -$bString -r -o$i -i$j -w$k"
				$(python Steg.py -$bString -r -o$i -i$j -w$k > ./_OUTPUTS/"$thing"/"$bString"-"$i"-"$j" 2>/dev/null) && echo -e "${COLOR}Success${NC}" && count=$((count+1)) || rm ./_OUTPUTS/"$thing"/"$bString"-"$i"-"$j"				
				
				#echo "Output is :$output"
				#echo "stegOut_0$(i)_$j"
			done
		done
	done
	rmdir _OUTPUTS/"$thing"
	$((thing++))
	echo -e "\n${COLOR}$count successful${NC}" 
done

