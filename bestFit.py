from Process import Process
import sys


class BestFit:
	def __init__(self, fpl, tms, fn, mmt):
		global AQ
		global EQ
		global memory
		global framesPerLine
		global totalMemSize
		global fileName
		global timeMemMove
		global freeMemory
		global largestOpenSlot
		global time
		AQ = []
		EQ = []
		memory = []
		fileName = fn
		framesPerLine = fpl
		totalMemSize = tms
		timeMemMove = mmt
		largestOpenSlot = tms
		freeMemory = tms

	def parsefile(self, filename):
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

	def sortArrivalQueue(self):
		AQ.sort(key=lambda x: (x.arrivalTime, x.pid), reverse=False)

	def sortExitQueue(self):
		EQ.sort(key=lambda x: (x[1], x[0]), reverse=False)

	def printArrivalQueueContents(self):
		for p in AQ:
			print(p)

	def printExitQueueContents(self):
		for p in EQ:
			print(p)

	def initializeMemory(self):
		for i in range(totalMemSize):
			memory.append('.')

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
		global memory
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
		return totalNumMoves,pidMoved

		# while 1:
		# 	# print(memory)
		# 	stateChange = 0
		# 	flag = 0
		# 	numMove = 0
		# 	currID = '.'
		# 	i = 0
		# 	for x in range(totalMemSize):
		# 		if memory[x] == '.' and flag == 0:
		# 			stateChange = 1
		# 			flag = 1
		# 		if flag == 1 and memory[x] != '.':
		# 			stateChange = 1
		# 			break
		# 	if stateChange == 0:
		# 		return 0
		# 	flag = 0
		# 	for x in range(totalMemSize):
		# 		if memory[x] == '.' and flag == 0:
		# 			flag = 1
		# 			numMove += 1
		# 		elif memory[x] == '.' and flag == 1:
		# 			numMove += 1
		# 		elif memory[x] != '.' and flag == 1:
		# 			flag = 0
		# 			currID = memory[x]
		# 			break
		# 		i += 1
		# 	if flag == 1:
		# 		return totalNumMoves, pidMoved
		# 	while 1:
		# 		if i == totalMemSize or memory[i] != currID:
		# 			break
		# 		else:
		# 			if memory[i] not in pidMoved:
		# 				pidMoved.append(memory[i])
		# 			memory[i - numMove] = memory[i]
		# 			memory[i] = '.'
		# 			totalNumMoves += 1
		# 		i += 1

	def addTime(self, s):
		global EQ, AQ
		for p in AQ:
			# print("BEFORE: " + str(p.arrivalTime))
			p.arrivalTime += s
		# print("AFTER: " + str(p.arrivalTime))

		d = dict(EQ)
		EQ = []
		for x in d.keys():
			d[x] += s
			EQ.append((x, d[x]))
		self.sortExitQueue()

	def bestFit(self, process):
		global freeMemory
		openSlots = []
		curStart = 0
		curSize = 0
		for i in range(totalMemSize):
			# We found an empty spot
			if (memory[i] == "."):
				# Either this is not the first one we found
				if (curSize > 0):
					curSize += 1
				# First position we found after a loaded memory seg
				else:
					curStart = i
					curSize = 1
			elif (curSize != 0 and memory[i] != "."):
				if (curSize >= process.memSize):
					openSlots.append((curStart, curSize))
				curSize = 0
		if (curSize >= process.memSize):
			openSlots.append((curStart, curSize))
			curSize = 0
		# So we didn't find any exact fits, so we need to find the smallest one
		smallestPos = 0
		smallestSize = 999999999
		for pair in openSlots:
			# print("pair[0]: "+str(pair[0])+" pair[1]:"+str(pair[1]))
			if pair[1] == process.memSize:
				smallestPos = pair[0]
				smallestSize = pair[1]
				break
			if (pair[1] < smallestSize):
				smallestPos = pair[0]
				smallestSize = pair[1]
		# print("freeMemory: "+str(freeMemory) +" removed: "+str(process.memSize))
		freeMemory -= process.memSize
		# print("Equal: "+str(freeMemory))
		for mem in range(process.memSize):
			memory[smallestPos + mem] = process.pid

	def calcLargestSlot(self):
		global largestOpenSlot
		counter = 0;
		largestSlot = 0
		for i in range(totalMemSize):
			if (memory[i] == "."):
				counter += 1
			else:
				largestSlot = max(counter, largestSlot)
				counter = 0
		largestSlot = max(counter, largestSlot)
		largestOpenSlot = largestSlot

	def removeFromMem(self, pid):
		global freeMemory
		counter = 0
		for i in range(totalMemSize):
			if (memory[i] == pid):
				memory[i] = "."
				counter += 1
		# print("freeMemory: " + str(freeMemory) + " removed: " + str(counter))
		freeMemory += counter
		# print("Equal : "+str(freeMemory))

	def simulate(self):
		global AQ, EQ, fileName, freeMemory, largestOpenSlot, timeMemMove
		self.parsefile(fileName)
		self.initializeMemory()
		self.sortArrivalQueue()
		time = 0
		print("time 0ms: Simulator started (Contiguous -- Best-Fit)")
		while len(AQ) > 0 or len(EQ) > 0:
			if len(EQ) > 0 and time == EQ[0][1]:
				process = EQ.pop(0)
				print("time " + str(time) + "ms: Process " + process[0] + " removed:")
				self.removeFromMem(process[0])
				self.calcLargestSlot()
				self.printMemory()
			elif AQ and time == AQ[0].arrivalTime:
				process = AQ.pop(0)
				print("time " + str(time) + "ms: Process " + process.pid + " arrived (requires " + str(
					process.memSize) + " frames)")
				if (process.memSize > freeMemory):
					print("time " + str(time) + "ms: Cannot place process " + process.pid + " -- skipped!")
				else:
					self.calcLargestSlot()
					if (process.memSize > largestOpenSlot):
						print("time " + str(
							time) + "ms: Cannot place process " + process.pid + " -- starting defragmentation")
						memMoved = self.defrag()
						totalTimeIncrease = memMoved[0] * timeMemMove
						time += totalTimeIncrease
						s = ""
						for i in range(len(memMoved[1])):
							if i == len(memMoved[1]) - 1:
								s += memMoved[1][i]
							else:
								s += memMoved[1][i]
								s += ", "
						print("time " + str(time) + "ms: Defragmentation complete (moved " + str(
							memMoved[0]) + " frames: " + s + ")")
						self.addTime(totalTimeIncrease)
						self.sortArrivalQueue()

					self.bestFit(process)
					self.calcLargestSlot()
					print("time " + str(time) + "ms: Placed process " + process.pid + ":")
					self.printMemory()
					EQ.append((process.pid, time + process.runTime))
					self.sortExitQueue()
			if AQ and EQ:
				time = min(AQ[0].arrivalTime, EQ[0][1])
			elif AQ:
				time = AQ[0].arrivalTime
			elif EQ:
				time = EQ[0][1]
		print("time " + str(time) + "ms: Simulator ended (Contiguous -- Best-Fit)")
