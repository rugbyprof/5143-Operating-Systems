#!/usr/local/bin/python3

"""
This file gives and idea of how to parse commands from the command prompt and
the invoke the proper command function with parameters. 

The functions are examples only that call the built in commands, which is not
acceptable for your project. Again, this file is just an example of parsing a 
command and calling the correct function with params.

It may give you a little insight into organizing your shell code as well.

"""
import threading
import sys
from subprocess import call  # FOR DEMO PURPOSES ONLY!


def cat(**kwargs):
    """Concatenate files and send to std out"""
    command = ["cat"]
    if "params" in kwargs:
        params = kwargs["params"]
    command.extend(params)
    call(command)


def ls(**kwargs):
    """Directory listing."""
    command = ["ls"]
    if "params" in kwargs:
        params = kwargs["params"]
    else:
        params = []
    command.extend(params)
    call(command)


def pwd(**kwargs):
    command = ["pwd"]
    if "params" in kwargs:
        params = kwargs["params"]
    else:
        params = []
    command.extend(params)
    call(command)


def exit(**kwargs):
    sys.exit()


class CommandHelper(object):
    def __init__(self):
        self.commands = {}
        self.commands["ls"] = ls
        self.commands["cat"] = cat
        self.commands["pwd"] = pwd
        self.commands["exit"] = exit

    def invoke(self, **kwargs):
        if "cmd" in kwargs:
            cmd = kwargs["cmd"]
        else:
            cmd = ""

        if "params" in kwargs:
            params = kwargs["params"]
        else:
            params = []

        if "thread" in kwargs:
            thread = kwargs["thread"]
        else:
            thread = False

        # One way to invoke using dictionary
        if not thread:
            self.commands[cmd](params=params)
        else:
            # Using a thread ****** broken right now *********
            if len(params) > 0:
                c = threading.Thread(target=self.commands[cmd], args=tuple(kwargs))
            else:
                c = threading.Thread(target=self.commands[cmd])

            c.start()
            c.join()

    def exists(self, cmd):
        print(self.commands)
        return cmd in self.commands


if __name__ == "__main__":

    ch = CommandHelper()

    while True:
        # get input from terminal (use input if raw_input doesn't work)
        cmd = input("$: ")

        # print(type(command_input))

        # remove command from params (very over simplified)
        # command_input = command_input.split()

        # params are all but first position in list
        # params = command_input[1:]

        # pull actual command from list
        # cmd = command_input[0]

        params = []

        # if command exists in our shell
        if ch.exists(cmd):
            ch.invoke(cmd=cmd, params=params, thread=False)
        else:
            print("Error: command %s doesn't exist." % (cmd))
