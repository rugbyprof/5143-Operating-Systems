import os
import sys


# keyword arguments
#positional args

def ls(**kwargs):
    name = kwargs.get('name',None)
    age = kwargs.get('age',None)
    gender = kwargs.get('gender',None)
    
    print(name,age,gender)
    
def rm(x):
    print(2*x)
    
    
if __name__ == '__main__':
    functions = {
        "ls":ls,
        "rm":rm
    }
    functions['ls'](gender="female",age=18,name="terry")
    functions['rm'](33)
    

    print(os.getcwd())
    print(os.path.isfile("06_join.py"))
    print(os.path.isdir("06_join.py"))