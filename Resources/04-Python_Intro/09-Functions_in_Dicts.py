"""
Functions as Variables

You can assign functions to variables in python. We can use this to leverage some "shell" organization in your main program of the shell assignment.

You could obviously use a huge `if then else` statement to achieve the same thing, but this will look cleaner.

Each function below has worthless filler just for this example.
"""

def ls(**kwargs):
    params = kwargs.get('params',None)
    flags = kwargs.get('flags',None)

    print(f"Function: ls, params: {params}, flags: {flags}")

def rm(**kwargs):
    params = kwargs.get('params',None)
    flags = kwargs.get('flags',None)

    print(f"Function: rm, params: {params}, flags: {flags}")

def mv(**kwargs):
    params = kwargs.get('params',None)
    flags = kwargs.get('flags',None)

    print(f"Function: mv, params: {params}, flags: {flags}")

def wc(**kwargs):
    params = kwargs.get('params',None)
    flags = kwargs.get('flags',None)

    print(f"Function: wc, params: {params}, flags: {flags}")


def driver(**kwargs):
    fname = kwargs.get('fname',None)
    params = kwargs.get('params',None)
    flags = kwargs.get('flags',None)

    function_lookup = {
        'ls':ls,
        'mv':mv,
        'rm':rm,
        'wc':wc
    }

    if fname:
        function_lookup[fname](params=params,flags=flags)


if __name__=='__main__':
    driver(fname='wc',flags='-l',params=['file1.txt','file2.csv'])
    driver(fname='mv',flags='-l',params=['from.txt','to.txt'])
    driver(fname='rm',flags='-rf',params=['dir_name'])