from Process import Process
import sys

AQ = []
EQ = []
memory = []

framesPerLine = int(sys.argv[1])
totalMemSize = int(sys.argv[2])
fileName = sys.argv[3]
memMoveTime = int(sys.argv[4])

freeMemory = totalMemSize
largestSlot = totalMemSize
prevAddPos = 0
time = 0


def printMemory():
    i = 0
    j = 0
    p = ""
    for a in range(framesPerLine):
        p += "="
    p += "\n"
    while 1:
        if i == totalMemSize:
            p += "\n"
            break
        if j == framesPerLine:
            p += "\n"
            j = 0
        p += memory[i]
        i += 1
        j += 1
    for a in range(framesPerLine):
        p += "="

    print(p)


def defrag():
    pidMoved = []
    totalNumMoves = 0
    while 1:
        # print(memory)
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
                numMove += 1
            elif memory[x] != '.' and flag == 1:
                flag = 0
                currID = memory[x]
                break
            i += 1
        if flag == 1:
            return totalNumMoves, pidMoved
        while 1:
            if i == totalMemSize or memory[i] != currID:
                break
            else:
                if memory[i] not in pidMoved:
                    pidMoved.append(memory[i])
                memory[i - numMove] = memory[i]
                memory[i] = '.'
                totalNumMoves += 1
            i += 1


def initMemory():
    for i in range(totalMemSize):
        memory.append('.')


def printParams():
    print(framesPerLine)
    print(totalMemSize)
    print(fileName)
    print(memMoveTime)


def parsefile(filename):
    data = open(filename).read()
    data = data.split('\n')
    for line in data:
        if line != "":
            line = line.split(' ')
            for i in range(2, len(line)):
                term = line[i].split('/')
                AQ.append(Process(line[0], int(line[1]), int(term[0]), int(term[1])))


def printArrivalQueueContents():
    for p in AQ:
        print(p)


def printExitQueueContents():
    for x in EQ:
        print(x)


def removeFromMemory(id):
    memRemoved = 0
    for i in range(totalMemSize):
        if memory[i] == id:
            memory[i] = '.'
            memRemoved += 1
    return memRemoved

def findNextSlot(size):
    global prevAddPos
    startingIndex = prevAddPos
    currentSize = 0
    flag = 0
    wrapped = False

    for i in range(startingIndex,totalMemSize):
        if memory[i] == '.' and currentSize == 0:
            startingIndex = i
            currentSize = 1
        elif memory[i] == '.' and currentSize > 0:
            currentSize += 1
            if currentSize == size:
                prevAddPos = startingIndex + size
                return startingIndex
        elif memory[i] != '.' and currentSize >0:
            if currentSize == size:
                prevAddPos = startingIndex + size
                return startingIndex
            currentSize = 0

    currentSize = 0
    startingIndex = 0

    # Need +1 to include the prevAddPos
    for i in range(0,totalMemSize):
        if memory[i] == '.' and currentSize == 0:
            startingIndex = i
            currentSize = 1
        elif memory[i] == '.' and currentSize > 0:
            currentSize += 1
            if currentSize == size:
                prevAddPos = startingIndex + size
                return startingIndex
        elif memory[i] != '.' and currentSize >0:
            if currentSize == size:
                prevAddPos = startingIndex + size
                return startingIndex
            currentSize = 0


def sortArrivalQueue():
    AQ.sort(key=lambda x: (x.arrivalTime,x.pid), reverse=False)


def nextFitPlace(p, t):
    s = p.memSize
    i = findNextSlot(s)
    for x in range(i, (i + s)):
        memory[x] = p.pid
    print("time " + str(t) + "ms: Placed process " + p.pid + ":")
    printMemory()


def addTime(s):
    global EQ
    global AQ
    for p in AQ:
        #print("BEFORE: " + str(p.arrivalTime))
        p.arrivalTime += s
        #print("AFTER: " + str(p.arrivalTime))

    d = dict(EQ)
    EQ = []
    for x in d.keys():
        d[x] += s
        EQ.append((x,d[x]))
    sortExitQueue()



def sortExitQueue():
     EQ.sort(key=lambda x: (x[1],x[0]), reverse=False)


def arrive(p, t):
    print("time " + str(t) + "ms: Process " + p.pid + " arrived (requires " + str(p.memSize) + " frames)")


def skip(p):
    global time
    print("time " + str(time) + "ms: " + "Cannot place process " + p.pid + " -- skipped!")
    for i in range(len(EQ)):
        if EQ[i][0] == p.pid:
            EQ.remove(i)


def exit(p, t):
    print("time " + str(t) + "ms: Process " + p[0] + " removed:")
    printMemory()


def calcLargestSlot():
    global largestSlot
    counter = 0;
    largestSlot = 0
    for i in range(totalMemSize):
        if (memory[i] == "."):
            counter += 1
        else:
            largestSlot = max(counter, largestSlot)
            counter = 0
    largestSlot = max(counter, largestSlot)

def simulate():
    global EQ
    global AQ
    global time
    global freeMemory
    global largestSlot
    print("time 0ms: Simulator started (Contiguous -- Next-Fit)")

    while len(AQ) > 0 or len(EQ) > 0:

        if len(EQ) > 0 and time == EQ[0][1]:
            freeMemory += removeFromMemory(EQ[0][0])
            print("time " + str(time) + "ms: Process " + EQ[0][0] + " removed:")
            printMemory()
            EQ.pop(0)
        elif len(AQ) > 0 and time == AQ[0].arrivalTime:
            currentProcess = AQ.pop(0)
            arrive(currentProcess, time)
            if currentProcess.memSize > freeMemory:
                skip(currentProcess)
            else:
                calcLargestSlot()
                if currentProcess.memSize > largestSlot:
                    print("time " + str(time) + "ms: " + "Cannot place process " + currentProcess.pid + " -- starting defragmentation")
                    add = defrag()
                    addTime(add[0]*memMoveTime)
                    time += add[0] * memMoveTime
                    s = ""
                    for i in range(len(add[1])):
                        if i == len(add[1]) - 1:
                            s += add[1][i]
                        else:
                            s += add[1][i]
                            s += ", "
                    print("time " + str(time) + "ms: " + "Defragmentation complete (moved " + str(add[0]) + " frames: " + s + ")")
                
                nextFitPlace(currentProcess, time)
                EQ.append((currentProcess.pid, time + currentProcess.runTime))
                sortExitQueue()
                freeMemory = freeMemory - currentProcess.memSize
                calcLargestSlot()
        if AQ and EQ:
            sortArrivalQueue()
            time = min(AQ[0].arrivalTime, EQ[0][1])
        elif AQ:
            sortArrivalQueue()
            time = AQ[0].arrivalTime
        elif EQ:
            sortArrivalQueue()
            time = EQ[0][1]
    print("time " + str(time) + "ms: Simulator ended (Contiguous -- Next-Fit)")

initMemory()

parsefile(fileName)
simulate()
# print("Done printing")
# sortArrivalQueue()
