#!/usr/bin/env python
from subprocess import call


def Cat(**kwargs):
    """
    params (list) : list of parameters

    DOCSTRING
    NAME
        cat - concatenate files and print on the standard output
    SYNOPSIS
        cat [OPTION]... [FILE]...
    DESCRIPTION
        Concatenate FILE(s) to standard output.

        -A, --show-all
                equivalent to -vET

        -b, --number-nonblank
                number nonempty output lines, overrides -n

        -e     equivalent to -vE

        -E, --show-ends
                display $ at end of each line

        -n, --number
                number all output lines

        -s, --squeeze-blank
                suppress repeated empty output lines

        -t     equivalent to -vT

        -T, --show-tabs
                display TAB characters as ^I

        --help display this help and exit

        --version
                output version information and exit
    EXAMPLES
        cat f - g
                Output f's contents, then standard input, then g's contents.

        cat    Copy standard input to standard output.
    """

    params = kwargs.get("params", [])
    flags = kwargs.get("flags", [])
    command = ["cat"]

    for f in params:
        command.append(f)

    call(command)

    if __name__ == "__main__":
        cat(files=["somefile", "otherfile"])
