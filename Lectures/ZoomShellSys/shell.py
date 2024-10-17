#!/usr/bin/env pythonpython
"""
This file is about using getch to capture input and handle certain keys 
when the are pushed. The 'command_DbApi.py' was about parsing and calling functions.
This file is about capturing the user input so that you can mimic shell behavior.

"""
import os
import sys
from time import sleep
from sqliteCRUD import SqliteCRUD

from getch import Getch
import requests


class DbApi:
    def __init__(self):
        self.url = "http://localhost:8080"
        self.conn = SqliteCRUD("fileSystem.db")

    def getId(self, name, pid=1):
        # http://localhost:8080/dirId?dir=data&pid=1
        res = requests.get(f"{self.url}/dirId/?dir={name}&pid={pid}")
        return res.json()

    def run_ls(self, cmd):
        params = cmd["params"]
        print(self.getId(params[0]))

    def run_cp(self, cmd):
        # already know what dir we are in
        #       cp dog pet (copy dog to pet in local directory)
        #       cp dog /other/dir/pet (copy dog to pet in other directory)
        #       cp dog /other/dir/pet/  (copy dog to directory pet keeping its own name dog)
        # get all the dog info from the db
        # insert that info into the pets folder
        pass


"""
- the shell allows users to enter commands
- we then parse the command and make function calls accordingly
    - simple commands would be implemented right here in this file (still possibly talking to the db)
    - more complex commands would be implemented and service using the api and the db
"""


##################################################################################
##################################################################################


getch = Getch()  # create instance of our getch class

DbApi = DbApi()

prompt = "$"  # set default prompt


def get_flags(cmd):
    flags = []
    for c in cmd:
        if c.startswith("-") or c.startswith("--"):
            flags.append(c)
    return flags


def get_params(cmd):
    params = []
    for c in cmd:
        if "-" in c or "--" in c:
            continue
        params.append(c)

    for i, p in enumerate(params[:-1]):
        if (
            params[i].startswith("'")
            and params[i + 1].endswith("'")
            or params[i].startswith('"')
            and params[i + 1].endswith('"')
        ):
            params[i] = params[i] + " " + params[i + 1]

    return params


def parse(cmd):
    """This function takes a command and parses it into a list of tokens
    1. Explode on redeirects
    2. Explode on pipes

    """
    redirect = None
    allCmds = []

    if ">" in cmd:
        cmd, redirect = cmd.split(">")
    if "|" in cmd:
        sub_cmds = cmd.split("|")
    else:
        sub_cmds = [cmd]

    for currCmd in sub_cmds:
        currCmd = currCmd.strip()
        currCmd = currCmd.split()

        allCmds.append(
            {
                "cmd": currCmd[0],
                "flags": get_flags(currCmd[1:]),
                "params": get_params(currCmd[1:]),
            }
        )
    if redirect:
        allCmds.append(
            {
                "cmd": ">",
                "flags": [],
                "params": [redirect.strip()],
            }
        )
    return allCmds


def print_cmd(cmd):
    """This function "cleans" off the command line, then prints
    whatever cmd that is passed to it to the bottom of the terminal.
    """
    padding = " " * 80
    sys.stdout.write("\r" + padding)  # clear the line
    sys.stdout.write("\r" + prompt + cmd)  # print the prompt and the command
    sys.stdout.flush()  # flush the buffer


if __name__ == "__main__":

    # cmd = "ls /home/user/griffin /www/html -l -a | grep 'student gpa' 'test.txt' '23,43,12' | wc -l > output.txt"  # empty cmd variable
    # print(cmd)
    # cmd = parse(cmd)

    # sys.exit(0)

    cmd = ""  # empty cmd variable

    print_cmd(cmd)  # print to terminal

    while True:  # loop forever

        char = getch()  # read a character (but don't print)

        if char == "\x03" or cmd == "exit":  # ctrl-c
            raise SystemExit("Bye.")

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
            print_cmd("")
            # This 'elif' simulates something "happening" after pressing return
            parsed_cmds = parse(cmd)
            print(parsed_cmds)
            sleep(1)

            # if parsed_cmd["cmd"] == "ls":
            #     print("Running ls command")
            #     DbApi.run_ls(parsed_cmd)
            # elif parsed_cmd["cmd"] == "pwd":
            #     DbApi.run_pwd(parsed_cmd)

            cmd = ""  # reset command to nothing (since we just executed it)

            print_cmd(cmd)  # now print empty cmd prompt
        else:
            cmd += char  # add typed character to our "cmd"
            print_cmd(cmd)  # print the cmd out
