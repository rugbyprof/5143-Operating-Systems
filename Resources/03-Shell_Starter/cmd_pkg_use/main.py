import os,sys

# get current working directory and append the cmd_pkg folder to the end
# this is so the import below can find it.
sys.path.append(os.path.join(os.getcwd(),'cmd_pkg'))

from cmd_pkg import *

cmd = CommandsHelper()

print(cmd.help['cat'])

