from Process import Process

class NextFit:

    def __init__(self, fpl, tms, fn, mmt):
        global framesPerLine
        global totalMemSize
        global fileName
        global memMoveTime
        global memory
        global AQ
        global EQ
        global framesPerLine
        global totalMemSize
        global freeMemory
        global largestSlot
        global time
        global prevAddPos
        framesPerLine = fpl
        totalMemSize = tms
        fileName = fn
        memMoveTime = mmt
        AQ = []
        EQ = []
        freeMemory = totalMemSize
        largestSlot = totalMemSize
        prevAddPos = 0
        memory = []
        time = 0


    def printMemory(self):
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


    def defrag(self):
        global memory,prevAddPos
        pidMoved = []
        existing = dict()
        totalNumMoves = 0
        slow = 0
        for fast in range(totalMemSize):
            if memory[fast] != '.':
                if fast > slow:
                    totalNumMoves += 1
                    if memory[fast] not in existing:
                        pidMoved.append(memory[fast])
                        existing[memory[fast]] = 1
                    memory[slow] = memory[fast]
                    memory[fast] = '.'
                slow += 1
        # self.printMemory()
        prevAddPos = slow
        return totalNumMoves,pidMoved
        # global memory
        # pidMoved = []
        # totalNumMoves = 0

        # while 1:
        #     # print(memory)
        #     stateChange = 0
        #     flag = 0
        #     numMove = 0
        #     currID = '.'
        #     i = 0
        #     for x in range(totalMemSize):
        #         if memory[x] == '.' and flag == 0:
        #             stateChange = 1
        #             flag = 1
        #         if flag == 1 and memory[x] != '.':
        #             stateChange = 1
        #             break
        #     if stateChange == 0:
        #         return 0
        #     flag = 0
        #     for x in range(totalMemSize):
        #         if memory[x] == '.' and flag == 0:
        #             flag = 1
        #             numMove += 1
        #         elif memory[x] == '.' and flag == 1:
        #             numMove += 1
        #         elif memory[x] != '.' and flag == 1:
        #             flag = 0
        #             currID = memory[x]
        #             break
        #         i += 1
        #     if flag == 1:
        #         global prevAddPos
        #         prevAddPos = 0
        #         for i in range(totalMemSize):
        #             if memory[i] != '.':
        #                 prevAddPos+=1
        #             else:
        #                 break
        #         return totalNumMoves, pidMoved
        #     while 1:
        #         if i == totalMemSize or memory[i] != currID:
        #             break
        #         else:
        #             if memory[i] not in pidMoved:
        #                 pidMoved.append(memory[i])
        #             memory[i - numMove] = memory[i]
        #             memory[i] = '.'
        #             totalNumMoves += 1
        #         i += 1



    def initMemory(self):
        global totalMemSize,memory
        for i in range(totalMemSize):
            memory.append('.')


    def printParams(self):
        print(framesPerLine)
        print(totalMemSize)
        print(fileName)
        print(memMoveTime)


    def parsefile(self,filename):
        data = open(filename).read()
        data = data.split('\n')
        for line in data:
            if line != "" and not line.startswith("#") and not line.startswith(" ") and not line.startswith("\t"):
                if ' ' in line:
                    line = line.split(' ')
                elif '\t' in line:
                    line = line.split('\t')
                for i in range(2, len(line)):
                    term = line[i].split('/')
                    AQ.append(Process(line[0], int(line[1]), int(term[0]), int(term[1])))


    def printArrivalQueueContents(self):
        for p in AQ:
            print(p)


    def printExitQueueContents(self):
        for x in EQ:
            print(x)


    def removeFromMemory(self,id):
        memRemoved = 0
        for i in range(totalMemSize):
            if memory[i] == id:
                memory[i] = '.'
                memRemoved += 1
        return memRemoved

    def findNextSlot(self,size):
        global prevAddPos
        startingIndex = prevAddPos
        currentSize = 0

        if(size == 0):
            return startingIndex

        for i in range(startingIndex,totalMemSize):
            if memory[i] == '.' and currentSize == 0:
                startingIndex = i
                currentSize = 1
                if currentSize == size:
                    prevAddPos = startingIndex + size
                    return startingIndex
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
        for i in range(totalMemSize):
            if memory[i] == '.' and currentSize == 0:
                startingIndex = i
                currentSize = 1
                if currentSize == size:
                    prevAddPos = startingIndex + size
                    return startingIndex
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


    def sortArrivalQueue(self):
        AQ.sort(key=lambda x: (x.arrivalTime,x.pid), reverse=False)


    def nextFitPlace(self,p, t):
        s = p.memSize
        i = self.findNextSlot(s)
        for x in range(i, (i + s)):
            memory[x] = p.pid
        print("time " + str(t) + "ms: Placed process " + p.pid + ":")
        self.printMemory()


    def addTime(self,s):
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
        self.sortExitQueue()



    def sortExitQueue(self):
         EQ.sort(key=lambda x: (x[1],x[0]), reverse=False)


    def arrive(self,p, t):
        print("time " + str(t) + "ms: Process " + p.pid + " arrived (requires " + str(p.memSize) + " frames)")


    def skip(self,p):
        global time
        print("time " + str(time) + "ms: " + "Cannot place process " + p.pid + " -- skipped!")
        for i in range(len(EQ)):
            if EQ[i][0] == p.pid:
                EQ.remove(i)


    def exit(self, p, t):
        print("time " + str(t) + "ms: Process " + p[0] + " removed:")
        self.printMemory()


    def calcLargestSlot(self):
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

    def simulate(self):
        global EQ
        global AQ
        global time
        global freeMemory
        global largestSlot
        self.initMemory()

        self.parsefile(fileName)
        print("time 0ms: Simulator started (Contiguous -- Next-Fit)")

        while len(AQ) > 0 or len(EQ) > 0:

            if len(EQ) > 0 and time == EQ[0][1]:
                freeMemory += self.removeFromMemory(EQ[0][0])
                print("time " + str(time) + "ms: Process " + EQ[0][0] + " removed:")
                self.printMemory()
                EQ.pop(0)
            elif len(AQ) > 0 and time == AQ[0].arrivalTime:
                currentProcess = AQ.pop(0)
                self.arrive(currentProcess, time)
                if currentProcess.memSize > freeMemory:
                    self.skip(currentProcess)
                else:
                    self.calcLargestSlot()
                    if currentProcess.memSize > largestSlot:
                        print("time " + str(time) + "ms: " + "Cannot place process " + currentProcess.pid + " -- starting defragmentation")
                        add = self.defrag()
                        self.addTime(add[0]*memMoveTime)
                        time += add[0] * memMoveTime
                        s = ""
                        for i in range(len(add[1])):
                            if i == len(add[1]) - 1:
                                s += add[1][i]
                            else:
                                s += add[1][i]
                                s += ", "
                        print("time " + str(time) + "ms: " + "Defragmentation complete (moved " + str(add[0]) + " frames: " + s + ")")

                    self.nextFitPlace(currentProcess, time)
                    EQ.append((currentProcess.pid, time + currentProcess.runTime))
                    self.sortExitQueue()
                    freeMemory = freeMemory - currentProcess.memSize
                    self.calcLargestSlot()
            if len(AQ) > 0 and len(EQ) > 0:
                self.sortArrivalQueue()
                time = min(AQ[0].arrivalTime, EQ[0][1])
            elif len(AQ) > 0:
                self.sortArrivalQueue()
                time = AQ[0].arrivalTime
            elif len(EQ) > 0:
                self.sortArrivalQueue()
                time = EQ[0][1]
        print("time " + str(time) + "ms: Simulator ended (Contiguous -- Next-Fit)")


