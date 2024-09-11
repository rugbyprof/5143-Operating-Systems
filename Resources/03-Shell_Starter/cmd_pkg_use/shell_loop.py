#!/usr/bin/env python
"""
This file is about using getch to capture input and handle certain keys 
when the are pushed. The 'command_helper.py' was about parsing and calling functions.
This file is about capturing the user input so that you can mimic shell behavior.

"""
import os
import sys
from time import sleep


from cmd_pkg import *
from cmd_pkg import CommandsHelper

cmdHelper = CommandsHelper()


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

getch = Getch()  # create instance of our getch class

prompt = "$"  # set default prompt


def print_cmd(cmd):
    """This function "cleans" off the command line, then prints
    whatever cmd that is passed to it to the bottom of the terminal.
    """
    padding = " " * 80
    sys.stdout.write("\r" + padding)
    sys.stdout.write("\r" + prompt + cmd)
    sys.stdout.flush()


if __name__ == "__main__":
    cmd = ""  # empty cmd variable

    print_cmd(cmd)  # print to terminal

    while True:  # loop forever

        char = getch()  # read a character (but don't print)

        if char == "\x03" or cmd == "exit":  # ctrl-c
            raise SystemExit("\nBye.")

        elif char == "\x7f":  # back space pressed
            cmd = cmd[:-1]
            print_cmd(cmd)

        elif char in "\x1b":  # arrow key pressed
            null = getch()  # waste a character
            direction = getch()  # grab the direction

            if direction in "A":  # up arrow pressed
                # get the PREVIOUS command from your history (if there is one)
                # prints out 'up' then erases it (just to show something)
                cmd += "\u2191"
                print_cmd(cmd)
                sleep(0.3)
                # cmd = cmd[:-1]

            if direction in "B":  # down arrow pressed
                # get the NEXT command from history (if there is one)
                # prints out 'down' then erases it (just to show something)
                cmd += "\u2193"
                print_cmd(cmd)
                sleep(0.3)
                # cmd = cmd[:-1]

            if direction in "C":  # right arrow pressed
                # move the cursor to the right on your command prompt line
                # prints out 'right' then erases it (just to show something)
                cmd += "\u2192"
                print_cmd(cmd)
                sleep(0.3)
                # cmd = cmd[:-1]

            if direction in "D":  # left arrow pressed
                # moves the cursor to the left on your command prompt line
                # prints out 'left' then erases it (just to show something)
                cmd += "\u2190"
                print_cmd(cmd)
                sleep(0.3)
                # cmd = cmd[:-1]

            print_cmd(cmd)  # print the command (again)

        elif char in "\r":  # return pressed

            # This 'elif' simulates something "happening" after pressing return
            # cmd = "Executing command...."   #

            # This code block is for demonstration purposes only
            # You should:
            #   1. Parse the command
            #       - Split on pipes to get sub commands
            #       - Handle each sub command by finding the:
            #           - Command
            #           - Arguments
            #           - Flags
            #   2. Execute the sub command by sending in the output of a previous command if it exists into the sub command
            #   3. Capture the output of the sub command
            #   4. Determine if there are more sub commands to execute and if not, print the output of the last sub command

            if cmd == "ls":
                print("running ls function")
            elif cmd == "pwd":
                print("running pwd function")
            elif cmd == "grep":
                print("running grep function")

            # No reason to sleep here, just showing you can
            sleep(1)

            ## YOUR CODE HERE
            ## Parse the command
            ## Figure out what your executing like finding pipes and redirects

            cmd = ""  # reset command to nothing (since we just executed it)

            print_cmd(cmd)  # now print empty cmd prompt
        else:
            cmd += char  # add typed character to our "cmd"
            print_cmd(cmd)  # print the cmd out
