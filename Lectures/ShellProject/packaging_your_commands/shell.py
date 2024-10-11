import importlib
import pkgutil
import cmd_pkg
from rich import print


# Dictionary to store the commands
cmds = {}


# Dynamically load all functions from cmd_pkg into the dictionary
def load_commands():
    global cmds

    # Loop through all modules in the cmd_pkg package
    for _, module_name, _ in pkgutil.iter_modules(cmd_pkg.__path__):
        module = importlib.import_module(f"cmd_pkg.{module_name}")

        # Loop through the attributes in each module
        for name in dir(module):
            obj = getattr(module, name)
            # Check if it's a callable function and doesn't start with '__'
            if callable(obj) and not name.startswith("__"):
                cmds[name] = obj


# Get the docstring of a function
def get_docstring(func_name):
    """
    Get the docstring of a function.

    :param func_name: The name of the function
    :return: The docstring of the function
    """

    if func_name in cmds:
        return cmds[func_name].__doc__
    else:
        return f"Function '{func_name}' not found."


if __name__ == "__main__":
    # Load the commands dynamically from cmd_pkg
    load_commands()

    print(cmds)
    # Example usage:
    cmd = "ls"
    params = ["/usr/local/bin"]

    # Call the function dynamically from the dictionary
    if cmd in cmds:
        result = cmds[cmd](params=params)
        print(result)
    else:
        print(f"Command '{cmd}' not found.")

    # help = cmds["cat"].__doc__.split("DOCSTRING")[1]
    # print(help)
