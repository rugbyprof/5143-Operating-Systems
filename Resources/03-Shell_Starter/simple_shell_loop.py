#!/usr/bin/env python
"""
Simple shell loop starter

The "Getch" code is directly pasted into this file so that everything is in one 
place and not split into multiple files. 

The only other function I left was a "print_cmd" function since printing the command
required 3 lines of code every time. Otherwise, all the code is inline (besides getch)

"""
import os
import sys
from time import sleep

##################################################################################
##################################################################################
class Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): 
        return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

##################################################################################
##################################################################################

getch = Getch()                             # create instance of our getch class

prompt = "%:"                               # set default prompt


def print_cmd(cmd):
    """ This function "cleans" off the command line, then prints
        whatever cmd that is passed to it to the bottom of the terminal.
    """
    padding = " " * 80
    sys.stdout.write("\r"+padding)
    sys.stdout.write("\r"+prompt+cmd)
    sys.stdout.flush()


if __name__ == '__main__':
    cmd = ""                                # empty cmd variable

    print_cmd(cmd)                          # print to terminal
    
    while True:                             # loop forever

        char = getch()                      # read a character (but don't print)

        if char == '\x03' or cmd == 'exit': # ctrl-c
            raise SystemExit("Bye.")
        
        elif char == '\x7f':                # back space pressed
            cmd = cmd[:-1]
            print_cmd(cmd)
            
        elif char in '\x1b':                # arrow key pressed
            null = getch()                  # waste a character
            direction = getch()             # grab the direction
            
            if direction in 'A':            # up arrow pressed
                # get the PREVIOUS command from your history (if there is one)
                # prints out '↑' then erases it (just to show something)
                cmd += '↑'
                print_cmd(cmd)
                sleep(0.3)
                cmd = cmd[:-1]
                
            if direction in 'B':            # down arrow pressed
                # get the NEXT command from history (if there is one)
                # prints out '↓' then erases it (just to show something)
                cmd += '↓'
                print_cmd(cmd)
                sleep(0.3)
                cmd = cmd[:-1]
            
            if direction in 'C':            # left arrow pressed    
                # move the cursor to the LEFT on your command prompt line
                # prints out '←' then erases it (just to show something)
                cmd += '←'
                print_cmd(cmd)
                sleep(0.3)
                cmd = cmd[:-1]

            if direction in 'D':            # right arrow pressed
                # moves the cursor to the RIGHT on your command prompt line
                # prints out '→' then erases it (just to show something)
                cmd += '→'
                print_cmd(cmd)
                sleep(0.3)
                cmd = cmd[:-1]
            
            print_cmd(cmd)                  # print the command (again)

        elif char in '\r':                  # return pressed 
            
            # This 'elif' simulates something "happening" after pressing return
            cmd = "Executing command...."   # 
            print_cmd(cmd)                  
            sleep(1)    
            cmd = ""                        # reset command to nothing (since we just executed it)

            print_cmd(cmd)                  # now print empty cmd prompt
        else:
            cmd += char                     # add typed character to our "cmd"
            print_cmd(cmd)                  # print the cmd out

