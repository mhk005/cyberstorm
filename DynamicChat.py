import socket
import sys
from time import time
from binascii import unhexlify

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

ip = "localhost"
port = 33338
timeList = []
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((ip,port))                
data = s.recv(4096)
times = []
while(data.rstrip("\n") != "EOF"):
    sys.stdout.write(data)
    sys.stdout.flush()
    t0 = time()
    data = s.recv(4096)
    t1 = time()
    timeList.append(round(t1-t0,3))
s.close()
if len(timeList) > 0:
    times.append(timeList[0])
else:
    print("no times received!!")
    quit()

for i in timeList:
    flag = True
    for j in times:
        if (i > (j - .01) and i < (j + .01)):
            flag = False
    if flag:
        times.append(i)

print "The times are "+str(times)
for time1 in times:
    for time2 in times:
        if time1 != time2:
            bin_string = []
            for i in timeList:
                if i > (time1 - .01) and i < (time1 + .01):
                    bin_string.append('1')
                elif i > (time2 - .01) and i < (time2 + .01):
                    bin_string.append('0')
            #fin_string = convEight(bin_string)
            print("If "+str(time1) + " was a 1 and "+str(time2)+" was a 0, the output is :"+ convEight(bin_string))
                    
