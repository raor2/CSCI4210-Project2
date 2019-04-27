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
    totalNumMoves = 0
    while 1:
        flag = 0
        numMove = 0
        currID = '.'
        i = 0
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


def sortArrivalQueue():
    AQ.sort(key=lambda x: x.arrivalTime, reverse=False)


def sortExitQueue():
    EQ.sort(key=lambda x: x[1], reverse=False)

def simulate():
    time = 0


initMemory()
printParams()
printMemory()
# parsefile(fileName)
# print("Done printing")
# sortArrivalQueue()


