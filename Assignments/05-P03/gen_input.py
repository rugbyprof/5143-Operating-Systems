#!/Users/griffin/.pyenv/shims/python3

import random
import sys

def mykwargs(argv):
    '''
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
    '''
    args = []
    kwargs = {}

    for arg in argv:
        if '=' in arg:
            key,val = arg.split('=')
            kwargs[key] = val
        else:
            args.append(arg)
    return args,kwargs

 # Arrival time,  Process ID, Number of CPU bursts (N), Bursts (cpu , io, ...)
def generate_file(**kwargs):
    process_id = 0
    time = 0
    
    fp = open("datafile.dat","w")

    # default values
    nj = kwargs.get('nj',100)
    mincpu = kwargs.get('mincpu',3)
    maxcpu = kwargs.get('maxcpu',8)
    minio = kwargs.get('minio',5)
    maxio = kwargs.get('maxio',15)
    minb = kwargs.get('minb',5)
    maxb = kwargs.get('maxb',8)   
    minat = kwargs.get('minat',1)
    maxat = kwargs.get('maxat',3)



    
    for time in range(nj):
        #print(f"time:{time}")
        jobs = random.randint(minat,maxat)        # num jobs at this time
        #print(f"jobs:{jobs}")
        for job in range(jobs):   
            fp.write(str(time)+' ')              
            cpub = random.randint(minb,maxb-1)  # num cpu bursts
            fp.write(f"{process_id} ")
            fp.write(f"{cpub} ")
            #print(f"burst:{cpub}")
            for burst in range(cpub-1):
                b = random.randint(mincpu,maxcpu)
                i = random.randint(minio,maxio)
                fp.write(str(b)+' ')
                fp.write(str(i)+' ')
            b = random.randint(mincpu,maxcpu)
            fp.write(str(b)+'\n')
            process_id += 1
        #fp.write('\n')
    fp.close()



def usage():
    # if params are required ... 
    print("Usage: ")
    print("\tNeeds these parameter: ")
    print("\t\tNumber of jobs (nj)")
    print("\t\tMin cpu burst length (mincpu)")  
    print("\t\tMax cpu burst length (maxcpu)")  
    print("\t\tMin io burst length (minio)")  
    print("\t\tMax io burst length (maxio)")  
    print("\t\tMin number of bursts (minb)")
    print("\t\tMax number of bursts (maxb)\n")
    print("\t\tMin jobs per arrival time (minat)\n")
    print("\t\tMax jobs per arrival time (maxat)\n")
    print("Command:")
    print("\tgen_input.py nj=N mincpu=N maxcpu=N minio=N maxio=N minb=N maxb=N minat=N maxat=N")
    sys.exit()

if __name__=='__main__':
    argv = sys.argv[1:]

    args,kwargs = mykwargs(argv)

    if '--help' in args:
        usage()


    print("Default values can be changed in the `generate_file` function. \n")
    print("However run this file with --help after filename to get a usage \n")
    print("\texample to change values from command line \n")
    print("Generating file with the following format:\n")
    print("\ttime pid num_cpu_bursts cpub_1 iob_1 cpub2 iob_2 ... cpubn \n")
    generate_file(**kwargs)


    

