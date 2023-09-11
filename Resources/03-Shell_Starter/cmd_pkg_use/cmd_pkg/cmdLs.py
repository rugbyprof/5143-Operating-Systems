#!/usr/bin/env python
import subprocess

def ls(**kwargs):
    """This is my manpage entry for the pwd command
    """
    result = subprocess.run(['ls','-lah'], stdout=subprocess.PIPE)
    
    return result.stdout.decode('utf-8')