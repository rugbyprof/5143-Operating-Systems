#!/usr/bin/env python
import subprocess

def pwd(**kwargs):
    """This is my manpage entry for the pwd command
    """
    result = subprocess.run(['pwd'], stdout=subprocess.PIPE)
    
    return result.stdout.decode('utf-8')


if __name__=='__main__':
    print(pwd())