import hashlib
import datetime
import sys

def timediff_code(sdiff):

	#We need to hash twice
	hash_one = hashlib.md5(str(sdiff)).hexdigest()
	hash_two = hashlib.md5(str(hash_one)).hexdigest()

	#I wanted the hash just in case the code changed
	print("\n" + hash_two)
	
	letters = ""
	numbers = ""

	for i in range(0,len(hash_two)):

		if(hash_two[i].isalpha() and len(letters)<2): 
			letters+=hash_two[i]

		if(not hash_two[-(i+1)].isalpha() and len(numbers)<2):
			numbers+=hash_two[-(i+1)]

		if(len(numbers)==2 and len(letters)==2):
			break
	return letters+numbers


#Read in the file for epoch time
timein = []
for line in sys.stdin:
	timein.append(line.strip())

#Epoch time parsing
etl = timein[0].split(" ")
etl = [int(x) for x in etl]

if(len(timein)==2):
	stl = timein[1].split(" ")
	stl = [int(x) for x in stl]

#a is our epoch time as a date
a = datetime.datetime(etl[0],etl[1],etl[2],etl[3],etl[4],etl[5])

#b is our current system time as a date
if(len(timein)==2):
	b = datetime.datetime(stl[0],stl[1],stl[2],stl[3],stl[4],stl[5])
else:
	b = datetime.datetime.now()


#Compute the difference in seconds
sdiff = (b-a).total_seconds()

sdiff_less = int(((sdiff//60)*60)-3600)
sdiff_norm = sdiff_less+3600
sdiff_more = sdiff_norm+3600
sdiff_utc = sdiff_less+3600+3600*5

#This might involve manually entering in 4 codes wildly before our 60 seconds is up
print(timediff_code(sdiff_less) + " :3600 behind local")
print(timediff_code(sdiff_norm) + " :local")
print(timediff_code(sdiff_more) + " :3600 ahead local")
print(timediff_code(sdiff_utc)  + " :UTC")
