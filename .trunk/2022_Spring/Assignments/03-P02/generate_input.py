#!/Users/griffin/.pyenv/shims/python3

import random
import sys
import json

cpu_counts = [1, 2, 4, 8]


class WeightedPriorities:
    def __init__(self, choiceType="even"):
        self.priorityChoiceWeights = {
            "low": [35, 25, 18, 15, 7],
            "even": [20, 20, 20, 20, 20],
            "high": [7, 15, 18, 25, 35],
        }
        self.choiceType = choiceType
        self.priorityChoiceList = []
        self.generateWeightedPriority(choiceType)

        self.nextPriority = 0  # index to walk through priorityChoiceList

    def generateWeightedPriority(self, customWeights=None):
        """generate a random priority using a weighted scheme.
        Param:
            choiceType (string):
                even             : random distribution with no bias
                high             : random distribution with bias toward high priorities
                low              :     "                            "   low priorities
            customWeights (list) : list of new weights, one weight per priority (should add to 100 but doesn't have to):
                [5,10,15,20,25,30] = priorities 1-6 with weights:
                    priority 1  5/105 or 0.04%
                    priority 2 10/105 or 0.09%
                    priority 3 15/105 or 0.14%
                    ...
                    priority 6 30/105 or 0.28%
        """

        weights = self.priorityChoiceWeights[self.choiceType]

        for i in range(len(weights)):
            self.priorityChoiceList.extend([i + 1] * weights[i])

        random.shuffle(self.priorityChoiceList)

        print(self.priorityChoiceList)

    def getNext(self):
        # choose the next priority from front of the list
        p = self.priorityChoiceList[self.nextPriority]

        # increment the index to the next priority
        self.nextPriority = (self.nextPriority + 1) % len(self.priorityChoiceList)
        return p


def mykwargs(argv):
    """
    Processes argv list into plain args and kwargs.
    Just easier than using a library like argparse for small things.
    Example:
        python file.py arg1 arg2 arg3=val1 arg4=val2 -arg5 -arg6 --arg7
        Would create:
            args[arg1, arg2, -arg5, -arg6, --arg7]
            kargs{arg3 : val1, arg4 : val2}

        Params with dashes (flags) can now be processed seperately
    Shortfalls:
        spaces between k=v would result in bad params
    Returns:
        tuple  (args,kargs)
    """
    args = []
    kwargs = {}

    for arg in argv:
        if "=" in arg:
            key, val = arg.split("=")
            kwargs[key] = val
        else:
            args.append(arg)
    return args, kwargs


# Arrival time,  Process ID, Number of CPU bursts (N), Bursts (cpu , io, ...)
def generate_file(**kwargs):
    process_id = 0
    time = 0

    ofile = kwargs.get("ofile", "datafile.dat")

    if "." in ofile:
        name, ext = ofile.split(".")
    else:
        name = ofile
        ofile = ofile + ".dat"

    fp = open(ofile, "w")

    jsonJobs = []

    # default values
    nj = int(kwargs.get("nj", 100))
    minCpuBT = kwargs.get("minCpuBT", random.randint(5, 10))
    maxCpuBT = kwargs.get(
        "maxCpuBT", random.randint(int(minCpuBT) + 3, int(minCpuBT) + 8)
    )
    minIOBT = kwargs.get("minIOBT", random.randint(10, 15))
    maxIOBT = kwargs.get("maxIOBT", random.randint(int(minIOBT), int(minIOBT) + 5))
    minNumBursts = kwargs.get("minNumBursts", random.randint(5, 8))
    maxNumBursts = kwargs.get(
        "maxNumBursts", random.randint(int(minNumBursts) + 3, int(minNumBursts) + 8)
    )

    minat = kwargs.get("minat", 1)
    maxat = kwargs.get("maxat", 3)
    # minp = kwargs.get("minp", 1)
    # maxp = kwargs.get("maxp", 5)
    prioWeights = kwargs.get("prioWeights", "even")  # even , high, low

    intBurstType = kwargs.get("intBurstType", "normal")

    if "cpu" in intBurstType:
        minCpuBT += 10
        maxCpuBT += 20
        minIOBT -= 9
        maxIOBT -= 9

    if "io" in intBurstType:
        minIOBT += 10
        maxIOBT += 20
        minCpuBT += 4
        maxCpuBT += 4

    prios = WeightedPriorities(prioWeights)

    while process_id < nj:
        jsonJob = {}
        # print(f"time:{time}")
        jobs = random.randint(minat, maxat)  # num jobs at this time
        # print(f"jobs:{jobs}")
        for job in range(jobs):
            fp.write(str(time) + " ")
            jsonJob["arrivalTime"] = time
            cpub = random.randint(minNumBursts, maxNumBursts - 1)  # num cpu bursts
            fp.write(f"{process_id} ")
            jsonJob["process_id"] = process_id
            priority = prios.getNext()
            fp.write(f"p{priority} ")
            jsonJob["priority"] = priority
            # fp.write(f"{cpub} ")

            ioBursts = []
            cpuBursts = []

            # print(f"burst:{cpub}")
            for burst in range(cpub - 1):
                b = random.randint(int(minCpuBT), int(maxCpuBT))
                i = random.randint(int(minIOBT), int(maxIOBT))
                fp.write(str(b) + " ")
                cpuBursts.append(b)
                fp.write(str(i) + " ")
                ioBursts.append(i)

            b = random.randint(int(minCpuBT), int(maxCpuBT))
            fp.write(str(b) + "\n")
            cpuBursts.append(b)

            jsonJob["cpuBursts"] = cpuBursts
            jsonJob["ioBursts"] = ioBursts

            # b = random.randint(minCpuBT, maxCpuBT)
            # fp.write(str(b) + "\n")
            # jsonJob["cpus"] = b
            process_id += 1
            if process_id >= nj:
                break
        jsonJobs.append(jsonJob)
        time += 1
        # fp.write('\n')
    fp.close()

    fp = open(name + ".json", "w")
    dumpMe = {}
    dumpMe["kwargs"] = kwargs
    dumpMe["jobs"] = jsonJobs

    json.dump(dumpMe, fp, indent=4)

    return jsonJobs


def usage():
    # if params are required ...
    print(
        "Usage: (All params have defaults, but can be changed with the following): \n"
    )

    # total number of jobs generated
    print("\tnj      \t: Number of jobs[1 - n]")

    # min/max cpu burst lengths (increase for cpu intensive processes and vice versa)
    print("\tminCpuBT \t: Min cpu burst length.  Usually single digits: [1 - 9]")
    print(
        "\tmaxCpuBT \t: Max cpu burst length. Whatever you want: [number larger than minCpuBT]"
    )

    # min/max io burst lengths (increase for io intensive processes and vice versa)
    print("\tminIOBT \t: Min io burst length. Usually single digits: [1 - 9]")
    print(
        "\tmaxIOBT \t: Max io burst length. Whatever you want: [number larger that minIOBT]"
    )

    # determine min and max number of bursts. Smaller means shorter run times easier debugging
    print("\tminNumBursts \t: Min number of bursts [1 - n]")
    print("\tmaxNumBursts \t: Max number of bursts [number larger than minNumBursts")

    # OR instead of min and max number of bursts, you can use "cpu or io". Cpu  will generate many
    # more cpu bursts than IO bursts, and vice versa.
    print(
        "\tintBurstType \t: Generate bursts based on cpu intensive or io intensive [cpu,io]"
    )

    # Per arrival time - means number of jobs with the SAME arrival time
    # Having more jobs show up at the same time adds complexity to the load handling.
    print("\tminat       \t: Min jobs per arrival time [1-n]")
    print("\tmaxat       \t: Max jobs per arrival time [number larger than minat")

    # Adjust per your priority requirements. Priorities 1-5 seems sufficient in most cases.
    print("\tminp       \t: Min priority [1-n]")
    print("\tmaxp       \t: Max priority [larger than minp]")

    # More high or low or random? Value is comma seperated values with percentage per weight
    # so with priorites 1-5 and a prioWeights = 20,20,20,20,20 you get 20 percent for each weight
    # Using even,low, or high requires using priorities 1-5.
    print("\tprioWeights \t: Priority weights [even,low,high]")

    print("\tofile       \t: Outfile Name will write the output to that file.")

    print("\nExample Commands:")
    print(
        """
\tgen_input.py ofile=filename.wut nj=N minCpuBT=N maxCpuBT=N minIOBT=N maxIOBT=N minNumBursts=N 
\tmaxNumBursts=N minat=N maxat=N minp=N maxp=N prioWeights=[even,high,low]\nor\n
\tgen_input.py ofile=filename.wut nj=N minCpuBT=N maxCpuBT=N minIOBT=N maxIOBT=N intBurstType=[cpu,io] 
\tminat=N maxat=N minp=N maxp=N prioWeights=[even,high,low]\nor\n
\tgenerate_input.py prioWeights=low intensiveBurstType=cpu ofile=datafile_cpu_intense.dat\nor\n
\tgenerate_input.py prioWeights=high intensiveBurstType=io ofile=datafile_io_intense.dat
         """
    )
    sys.exit()


if __name__ == "__main__":
    argv = sys.argv[1:]

    args, kwargs = mykwargs(argv)

    if "--help" in args:
        usage()

    print("Default values can be changed in the `generate_file` function. \n")
    print("However run this file with `--help` after filename to get a usage ")
    print("example to change values from command line \n")
    print("Generating file with the following format:\n")
    print("\ttime pid priority cpub_1 iob_1 cpub2 iob_2 ... cpub_n \n")
    generate_file(**kwargs)
