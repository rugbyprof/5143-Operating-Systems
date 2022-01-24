import os
import sys


def ls(**kwargs):
    """Incorrect ls implementation as an example of how to pass params
        to this function and how to process flags and params

    Args:
        kwargs:
          flags (string): flags to alter the command
          params (list) : list of directories (or none) to do a listing with

    Returns:
        string: result of listing
    """

    params = kwargs.get("params", None)
    flags = kwargs.get("flags", None)

    if flags:
        pass

    listing = []

    if params:
        for dir in params:
            out = os.listdir(dir)
            for file in out:
                listing.append(file)
    else:
        listing = os.listdir(".")

    return listing


def cat():
    pass


def pwd():
    pass


def executeCommand(**kwargs):
    """Gets command flags and params and decides which function to call

    Returns:
        string: result of command
    """
    cmd = kwargs.get("cmd", None)
    params = kwargs.get("params", None)
    flags = kwargs.get("flags", None)

    commands = {}
    commands["ls"] = ls
    commands["cat"] = cat
    commands["pwd"] = pwd

    result = commands[cmd](params=params, flags=flags)

    return result


if __name__ == "__main__":
    """Assumes a command is of the following format:
    cmd -flags param1 param2 ... paramN
    """
    cmd = None
    flags = None
    params = None

    buffer = input()  # read input
    buffer = buffer.strip()  # clean off whitespace front and back
    buffer = buffer.split()  # split on spaces

    cmd = buffer[0]  # command is assumed to be first item
    if len(buffer) > 1:
        flags = buffer[1]  # flags are assumed to be next
    if len(buffer) > 2:
        params = buffer[2:]  # params are assumed to be after

    result = executeCommand(cmd=cmd, flags=flags, params=params)
    print(result)


###### KWARGS STUFF FROM CLASS...
# def printPerson(**kwargs):
#   first = kwargs.get("first",None)
#   last = kwargs.get("last",None)
#   age = kwargs.get("age",None)
#   sex = kwargs.get("sex",None)

#   if first and last and age and sex:
#     print(first,last,age,sex)


# if __name__=='__main__':
#   printPerson(age=99,sex="don't ask",showSize="american or european?",first="Rashid",last="Pirapally")
