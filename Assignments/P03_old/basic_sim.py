timeSlice = 2

class Queue:
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ",".join(self.queue)

    def addPCB(self,pcb):
        self.queue.append(pcb)
    
    def removePCB(self):
        item = self.queue[0]
        del self.queue[0]
        return item

    def decrement(self):
        """ Iterate over the self.queue and decrement or call whatever
            method for each of the pcb's in this queue
        """
        # for each process in queue
        #    call decrementIoBurst
        pass
    
    def incrememnt(self,what='waittime'):
        """ Iterate over the self.queue and decrement or call whatever
            method for each of the pcb's in this queue
        """
        # for each process in queue
        #    call incrementwaittime
        if what =='waittime':
            pass
        elif what == 'runtime':
            pass
        pass

class SysClock:
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state
        if not 'clock' in self.__dict__: 
            self.clock = 0
    

class CPU:
    def __init__(self):
        self.busy = False
        self.runningPCB = None

    def decrementCurrentProcess(self):
        self.runningPCB.decrementCpuBurst()
    
    def loadProcess(self,pcb):
        self.runningPCB = pcb

    def testKickOff(self):
        if self.runningPCB.getCurrentBurstTime() == 0:
            pass
            # kick it off the cpu




class PCB:
    def __init__(self,pid,bursts,at,priority):
        self.pid = pid     
        self.priority = priority     # 0
        self.arrivalTime = at
        self.bursts = bursts    # 5 3  2 2  2 3  3 3 3 2 3 3 4 2 5 2 5 3 3 3 4
        self.currBurst = 'IO'
        self.currBurstIndex = 1
        self.cpuBurst = 5
        self.readyQueueTime = 0
        self.waitQueueTime = 0
        self.cpuTime = 0

    def decrementCpuBurst(self):
        self.bursts[self.currBurstIndex] -= 1

    def decrementIoBurst(self):
        self.bursts[self.currBurstIndex] -= 1

    def incrementBurstIndex(self):
        self.currBurstIndex += 1
    
    def getCurrentBurstTime(self):
        return self.bursts[self.currBurstIndex]
    
class Simulator:
    def __init__(self,datfile):
        self.datfile = datfile
        self.new = Queue()
        self.wait = Queue()
        self.running = CPU()
        self.ready = Queue()
        self.terminated = Queue()
        self.readData()

    def __str__(self):
        s = ""
        s += "datfile: "+self.datfile +"\n"
        s += "new queue: "+",".join(self.new)  +"\n"
        s += "wait: "+",".join*(self.wait)  +"\n"
        return s


    def readData(self):
        with open(self.datfile) as f:
            self.data = f.read().split("\n")

        for process in self.data:
            if len(process) > 0:
                parts = process.split(' ')
                arrival = parts[0]
                pid = parts[1]
                priority = parts[2]
                bursts = parts[3:]

                print(f"{arrival}, {pid}, {priority} {len(bursts)}{bursts}")


if __name__=='__main__':
    sim = Simulator("datafile.dat")
    print(sim)