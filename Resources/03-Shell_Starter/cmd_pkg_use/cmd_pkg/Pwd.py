#!/usr/bin/env python
from subprocess import call

def Pwd(**kwargs):
    print("\n")
    call(["pwd"])


if __name__=='__main__':
    print(Pwd())