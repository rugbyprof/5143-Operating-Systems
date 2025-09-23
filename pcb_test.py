

class PCB:
    def __init__(self,start,bursts,id):
        self.start = start
        self.bursts= bursts
        self.pid = id
        self.waitq_count=0
        self.readyq_count=0
        self.running = 0
        self.io = 0

    def __repr__(self):
        return str(self.pid)+" "+str(self.readyq_count)


if __name__=='__main__':

    jobs = [PCB(0,[3,2,3],1),PCB(1,[2,2,3],2),PCB(2,[2,2,3],3)]

    readyQ= []
    cpuQ = []
    waitQ = []
    ioQ = []
    clock = 0
    exit = []

    print(jobs)


    for i in range(len(jobs)):
        print(jobs[i])
        if jobs[i].start == clock:
            readyQ.append(jobs[i])
        print(i)
        clock += 1

    for job in readyQ:
        job.readyq_count += 1

    print(readyQ)

    readyTotal = 0
    for job in readyQ:
        readyTotal += job.readyq_count

    print(readyTotal)





