# cmd_pkg/pwd.py

import os


def grep(pattern, file):
    return os.grep(pattern, file)


if __name__ == "__main__":
    grep("*.txt", "somefile.txt")
