from Process import Process
import sys

AQ = []
EQ = []
framesPerLine = int(sys.argv[1])
totalMemSize = int(sys.argv[2])
freeMemory = totalMemSize
largestSlot = totalMemSize
fileName = sys.argv[3]
memMoveTime = int(sys.argv[4])
memory = []
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
                EQ.append((line[0], int(term[1])))


def printArrivalQueueContents():
    for p in AQ:
        print(p)


def printExitQueueContents():
    for x in EQ:
        print(x)


def removeFromMemory(id):
    for i in range(totalMemSize):
        if memory[i] == id:
            memory[i] = '.'


def findFirstSlot(size):
    startingIndex = 0
    currentSize = 0
    flag = 0

    for i in range(totalMemSize):
        print(startingIndex)
        if memory[i] == '.' and flag == 0:
            flag = 1
            currentSize += 1
            startingIndex = i

        elif memory[i] == '.' and flag == 1:
            currentSize += 1
            if currentSize >= size:
                return startingIndex
        elif memory[i] != '.' and flag == 1:
            flag = 0
            if currentSize == size:
                return startingIndex


def sortArrivalQueue():
    AQ.sort(key=lambda x: x.arrivalTime, reverse=False)


def firstFitPlace(p, t):
    s = p.memSize
    i = findFirstSlot(s)
    for x in range(i, (i + s)):
        memory[x] = p.id


def sortExitQueue():
    EQ.sort(key=lambda x: x[1], reverse=False)


def arrive(p, t):
    print("time " + t + "ms: Process" + p.id + " arrived  (requires " + p.memSize + " frames)")


def exit(p, t):
    print("time " + t + "ms: Process " + p[0] + " removed:")
    printMemory()


def simulate():
    print("time 0ms: Simulator started (Contiguous -- First-Fit)")

    while len(AQ) > 0 or len(EQ) > 0:
        if(len(EQ) > 0 and time == EQ[0][1]):



initMemory()
printParams()
printMemory()
# parsefile(fileName)
# print("Done printing")
# sortArrivalQueue()
