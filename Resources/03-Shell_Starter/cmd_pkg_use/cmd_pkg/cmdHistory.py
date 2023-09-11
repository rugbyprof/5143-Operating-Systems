#!/usr/bin/env python
import subprocess
import readline; 
def history(**kwargs):
    """This is my man page entry for the history command
    """


    print('\n'.join([str(readline.get_history_item(i + 1)) for i in range(readline.get_current_history_length())]))


if __name__=='__main__':
    print("\n")
    history()