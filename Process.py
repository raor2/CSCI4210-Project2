class Process:



    def __init__(self,id,mem,arrivialTime,runTime):
        self.pid = id
        self.memSize = mem
        self.arrivialTime = arrivialTime
        self.runTime = runTime


    def __repr__(self):
        ret = "Process ID: " + str(self.pid) + "\nMemory Size: " + str(self.memSize) + "\nArrivial Time: " + str(self.arrivialTime) + "\nRun Time: " + str(self.runTime) + "\n"
        return return

    
