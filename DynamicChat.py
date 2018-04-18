###########################################################################
# Name : Dynamic Covert Chat
# Author: Team Patience, CSC 442
# Description: Dynamically detects time intervals sent from a chat server
#              and forms a binary message.
# Parameters: python DynamicChat.py
# Dynamic Input : Different input-Change the precision of time readings
#                 Hostname - specify specific host to connect to
#                 Port - Specify different port then 31337
#
# Dynamic format syntax : python DynamicChat.py TimeInterval IP Port
###########################################################################


import socket
import sys
from time import time
from binascii import unhexlify


#Sets pre-set interval, ip, and port
INTERVAL = .02
ip = "jeangourd.com"
port = 31337

#Optional Parameters
#Must specify parameters in command line if you'd like to change from preset
# Intervals take into account any random small margins of error in delays
#server communication. If the argument is null, the program runs with the default
try:
    if sys.argv[1] != None:
        INTERVAL = float(sys.argv[1])
    if sys.argv[2] != None:
        ip = sys.argv[2]
    if sys.argv[3] != None:
        port = int(sys.argv[3])
except:
    pass


def convEight(binary):

    #Builds an array of characters to be joined at end into string.
    #I used an array because its trivial to pop the last element in the case
    #of a backspace 
    endString = []

    #Backspace character being matched
    backspace = '00001000'
    #run while the input is less then 8 characters left, as its the end of 
    # input
    while len(binary) >= 8:
	
	#The first eight elements of list are popped into a temp subset
        subset = binary[0:8]
	
	#If the backspace character is matched, pop the string
        if ''.join(subset) == backspace and len(endString) != 0:
            endString.pop()
        else:
	
	    #Else, join the list, use int function to convert to binary, then 
	    #chr to represent the ascii value associated with the binary number
            endString.append((chr(int(''.join(subset),2))))
	#At the end, pop off the first eight elements and continue with the looping
        del binary[:8]
    #return the final string
    return(''.join(endString))

#Start with an empty timeList, this will later be populated
timeList = []

#Initalize time array
times = []

#Create a new socket, running on IPV4 and using TCP for communcation method
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#Connect to the specified IP and port from earlier
s.connect((ip,port))

#Store the value received from the server in data
data = s.recv(4096)


#Continue reading information until you reach EOF string, meaning string is complete
while(data.rstrip("\n") != "EOF"):

    #Write the data coming from the server
    sys.stdout.write(data)

    #flush standard output to allow other data 
    sys.stdout.flush()

    #Initalize time as current time before data is received
    t0 = time()

    #receive the next letter in sequence
    data = s.recv(4096)

    #Record the time after data is recieved
    t1 = time()

    #append the recorded time to timeList array.
    timeList.append(round(t1-t0,3))

#We no longer need the socket, so sucessfully close it.
s.close()

#If we received any info, add the first time received to the list of individual times
if len(timeList) > 0:
    times.append(timeList[0])
else:
    print("no times received!!")
    quit()

#Cycles through the entire list of times received from the server
for i in timeList:
    flag = True
    #Cycle through the current times being saved into times array. At the start
    #there is only one value, but more values are added later, dynamically
    #allowing the for loop to cover those times as well.
    for j in times:

        #If the value in the list of recorded times is within the defined interval of
        # a time already stored in our saved times, set the flag to be False.
        #This is weird, but some times are within the interval of one time, but
        #could still be totally different then other times. As a result, if its close
        #to any of the times, we don't need to add it.
        if (i > (j - INTERVAL) and i < (j + INTERVAL)):
            flag = False
    #If flag is still true at this point, it means that the time being compared
    # is not already in our saved times, so add it.
    if flag:
        times.append(i)
#At the end of the previous for loops, you are left with a smaller array with
# all the independent times being sent from the server.
print "The times are "+str(times)

#Cycles through all of the times in the Saved Times list
for time1 in times:

    #Also, cycles through all of the times in the Saved Times list, allowing you to compare each value
    #compare all of the times in the list to one another.
    for time2 in times:

        #Both time's cannot represent a 1 and 0, so if they are the same time, skip that iteration.
        if time1 != time2:

            #Initialize a new list bin_string
            bin_string = []

            #Cycle through the list of times received from server
            for i in timeList:

                #If the time is within the given interval of the time in
                #the for loop, append a 1 to your string
                if i > (time1 - INTERVAL) and i < (time1 + INTERVAL):
                    bin_string.append('1')
                #If your second time is within the given interval, append a
                #0 to your binary string
                elif i > (time2 - INTERVAL) and i < (time2 + INTERVAL):
                    bin_string.append('0')

            #At the end, you have a binary string that releates to two of the times coming from the server.
            #Because the entire program is dynamic, it can take any amount of different times from the server
            #It will try all possible combinations between times, as any of them could represent the 0 or 1, while other
            #times could be nonsensical. From there, you can look at the command line and view which output is correct.
            print("If "+str(time1) + " was a 1 and "+str(time2)+" was a 0, the output is :"+ convEight(bin_string))
                    
