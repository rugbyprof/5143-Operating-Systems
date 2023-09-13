import os,sys


# get current working directory and append the cmd_pkg folder to the end
# this is so the import below can find it.
sys.path.append(os.path.join(os.getcwd(),'cmd_pkg'))

from cmd_pkg import *
from cmd_pkg.cmdLs import ls 

# from cmd_pkg import commandsHelper

cmdHelper = CommandsHelper()

if __name__=='__main__':
    # cmd = sys.argv[1]

    # if cmd != 'help':
    #     result = cmdHelper.run(cmd)
    # else: 
    #     result = cmdHelper.help[sys.argv[2]]
    # print(result)

    print(ls())


