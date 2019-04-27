class Process:
    def __init__(self,id,mem,arrivaltime,runtime):
        self.pid = id
        self.memSize = mem
        self.arrivalTime = arrivaltime
        self.runTime = runtime

    def __repr__(self):
        ret = "Process ID: " + str(self.pid) + "\nMemory Size: " + str(self.memSize) + "\nArrivial Time: " + str(self.arrivalTime) + "\nRun Time: " + str(self.runTime) + "\n"
        return ret
