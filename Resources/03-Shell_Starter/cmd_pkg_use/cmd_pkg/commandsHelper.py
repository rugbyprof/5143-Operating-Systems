import os,sys

sys.path.append(os.getcwd())

# from ls import Ls
# from pwd import Pwd
# from cat import Cat

# from Grep import grep
# from Exit import exit 
# from History import history


class CommandsHelper(object):
    """
    This function iterates over globals.items() and if one of the values is "callable"
    meaning it is a function, then I add it to a dictionary called 'invoke'. I also
    add the functions '__doc__' string to a help dictionary.

    Methods:
        exists (string) : checks if a command exists (dictionary points to the function)
        help (string) : returns the doc string for a function 
    """
    def __init__(self):
        self.invoke = {}
        self.help = {}

        for key, value in globals().items():
            if key != 'Commands' and callable(value):
                self.invoke[key] = value
                self.help[key] = value.__doc__

    def exists(self,cmd):
        return cmd in self.invoke
    
    def help(self,cmd):
        return self.commands.invoke[cmd].__doc__
    
        

if __name__=='__main__':
    print("hello")
    print(os.getcwd())
    print(globals().items())
