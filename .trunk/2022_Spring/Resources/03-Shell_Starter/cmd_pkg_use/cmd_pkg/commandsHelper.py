#!/usr/bin/env python
from cmd_pkg.Ls import ls
from cmd_pkg.Pwd import pwd
from cmd_pkg.Cat import cat
# from Grep import grep
# from Exit import exit 
# from History import history

"""
This function iterates over globals.items() and if one of the values is "callable"
meaning it is a function, then I add it to a dictionary called 'invoke'. I also
add the functions '__doc__' string to a help dictionary.

Methods:
    exists (string) : checks if a command exists (dictionary points to the function)
    help (string) : returns the doc string for a function 
"""
class CommandsHelper(object):
    def __init__(self):
        self.invoke = {}
        self.help = {}

        for key, value in globals().items():
            if key != 'Commands' and callable(value):
                self.invoke[key] = value
                self.help[key] = value.__doc__

    def exists(self,cmd):
        return cmd in self.invoke
    
    # def help(self,cmd):
    #     return self.commands.invoke[cmd].__doc__
    
        

if __name__=='__main__':
    pass
