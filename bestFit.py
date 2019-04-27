from Process import Process
import sys


AQ = []
EQ = []
memory = []

framePerLine = int(sys.argv[1],10)
totalMemSize = int(sys.argv[2],10)
timeMemMove = int(sys.argv[3],10)
largestOpenSlot = totalMemSize
freeMemory = totalMemSize


def parsefile(filename):
    data = open(filename).read()
    data = data.split('\n')
    for line in data:
        if line != "":
            line = line.split(' ')
            for i in range(2, len(line)):
                term = line[i].split('/')
                AQ.append(Process(line[0], int(line[1]), int(term[0]), int(term[1])))

def sortArrivalQueue():
    AQ.sort(key=lambda x: x.arrivalTime, reverse=False)

def printArrivalQueueContents():
    for p in AQ:
        print(p)

def initializeMemory():
	for i in range(totalMemSize):
		memory.append(".")

def printMemory():
	for header in range(framePerLine):
		sys.stdout.write("=")
	sys.stdout.write("\n")

	for pos in range (totalMemSize):
		sys.stdout.write(memory[pos])
		if (pos + 1) % framePerLine == 0:
			sys.stdout.write('\n')

	for header in range(framePerLine):
		sys.stdout.write("=")
	sys.stdout.write("\n")

def sortExitQueue():
    EQ.sort(key=lambda x: x[1], reverse=False)

def defrag():
    totalNumMoves = 0
    while 1:
        #print(memory)
        stateChange = 0
        flag = 0
        numMove = 0
        currID = '.'
        i = 0
        for x in range(totalMemSize):
            if memory[x] == '.' and flag == 0:
                stateChange = 1
                flag = 1
            if flag == 1 and memory[x] != '.':
                stateChange = 1
                break
        if stateChange == 0:
            return 0
        flag = 0
        for x in range(totalMemSize):
            if memory[x] == '.' and flag == 0:
                flag = 1
                numMove += 1
            elif memory[x] == '.' and flag == 1:
                numMove+=1
            elif memory[x] != '.' and flag == 1:
                flag = 0
                currID = memory[x]
                break
            i+=1
        if flag == 1:
            return totalNumMoves
        while 1:
            if i == totalMemSize or memory[i] != currID:
                break
            else:
                memory[i-numMove] = memory[i]
                memory[i] = '.'
                totalNumMoves += 1
            i+=1


def removeFromMem(pid):
	global freeMemory
	counter = 0
	for i in range(totalMemSize):
		if(memory[i] == pid):
			memory[i] = "."
			counter+=1
	freeMemory+=counter


def bestFit(process):
	openSlots = []
	curStart = 0
	curSize = 0
	global freeMemory
	for i in range(totalMemSize):
		# We found an empty spot
		if(memory[i] == "."):
			# Either this is not the first one we found
			if(curSize > 0):
				curSize = curSize + 1
			# First position we found after a loaded memory seg
			else:
				curStart = i
				curSize = 1
		elif(curSize != 0 and memory[i] != "."):
			if ( curSize >= process.memSize):
				openSlots.append((curStart,curSize))
				curSize = 0
	if ( curSize >= process.memSize):
		openSlots.append((curStart,curSize))
		curSize = 0
	# So we didn't find any exact fits, so we need to find the smallest one
	smallestPos = 0
	smallestSize = sys.maxint
	for pair in openSlots:
		# print("pair[0]: "+str(pair[0])+" pair[1]:"+str(pair[1]))
		if(pair[1] == process.memSize):
			smallestPos = pair[0]
			smallestSize = pair[1]
			break
		if(pair[1]<smallestSize):
			smallestPos = pair[0]
			smallestSize = pair[1]

	freeMemory = freeMemory - process.memSize
	for mem in range(process.memSize):
		memory[smallestPos+mem] = process.pid

def calcLargestSlot():
	global largestOpenSlot
	counter = 0;
	largestSlot = 0
	for i in range(totalMemSize):
		if(memory[i] == "."):
			counter+=1
		else:
			largestSlot = max(counter,largestSlot)
			counter = 0
	largestSlot = max(counter,largestSlot)
	largestOpenSlot = largestSlot

def simulate():
    time = 0
    global freeMemory
    global largestOpenSlot
    global timeMemMove
    print("time 0ms: Simulator started (Contiguous -- Best-Fit)")
    while(AQ or EQ):
    	if(EQ and (time == EQ[0][1])):
    		process = EQ.pop(0)
    		print("time "+str(time)+"ms: Process "+process[0]+" removed:")
    		removeFromMem(process[0])
    		calcLargestSlot()
    		printMemory()
    	elif(AQ and time == AQ[0].arrivalTime):
    		process = AQ.pop(0)
    		print("time "+str(time)+"ms: Process "+process.pid+" arrived (requires "+str(process.memSize)+" frames)")
    		if(process.memSize > freeMemory):
    			print("time "+str(time)+"ms: Cannot place process "+process.pid+" -- skipped!")
    		else:
    			if( process.memSize > largestOpenSlot ):
    				print("time "+str(time)+"ms: Cannot place process "+process.pid+" -- starting defragmentation")
    				memMoved = defrag()
    				totalTimeIncrease = memMoved * timeMemMove

    			bestFit(process)
    			calcLargestSlot()
    			print("time " + str(time) + "ms: Placed process " + process.pid + ":")
    			printMemory()
    			EQ.append((process.pid,time + process.runTime))
    			sortExitQueue()
    			calcLargestSlot()
    	if(AQ and EQ):
    		time = min(AQ[0].arrivalTime,EQ[0][1])
    	elif(AQ):
    		time = AQ[0].arrivalTime
    	elif(EQ):
    		time = EQ[0][1]
    print("time " + str(time) + "ms: Simulator ended (Contiguous -- Best-Fit)")



parsefile("p2-input02.txt")
sortArrivalQueue()
# printArrivalQueueContents()
initializeMemory()
simulate()
