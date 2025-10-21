# cmd_pkg/pwd.py

import os


def Grep(pattern, file):
    return os.grep(pattern, file)


if __name__ == "__main__":
    Grep("*.txt", "somefile.txt")
    Grep("*.py", "otherfile.py")    