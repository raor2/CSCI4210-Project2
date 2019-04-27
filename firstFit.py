from Process import Process
import sys


AQ = []
EQ = []


def parsefile(filename):
    data = open(filename).read()
    data = data.split('\n')
    for line in data:
        if line != "":
            line = line.split(' ')
            print(line)
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





parsefile("p2-input03.txt")
print("Done printing")
sortArrivalQueue()
printArrivalQueueContents()

