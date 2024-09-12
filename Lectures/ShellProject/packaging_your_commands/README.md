## Python Packages

To organize your Python shell project and create a structure where all the shell commands are stored in a package or module, you can follow the steps below. This will allow you to either:

1. **Import all commands** with `from cmd_pkg import *`.
2. **Import individual commands** like `from cmd_pkg import pwd`.

### Directory Structure

You’ll need to organize the package using the following folder structure:

```
my_shell_project/
│
├── shell.py
├── cmd_pkg/
│   ├── __init__.py
│   ├── pwd.py
│   ├── ls.py
│   ├── echo.py
```

### Step-by-Step Breakdown

1. **`my_shell_project/`**: This is your project’s root folder.
2. **`cmd_pkg/`**: This folder contains the Python package where all the shell command implementations will reside.
3. **`__init__.py`**: This file initializes the `cmd_pkg` package and can be used to expose or import commands from individual modules (like `pwd.py`, `ls.py`, etc.).
4. **`pwd.py`, `ls.py`, `echo.py`**: These are the modules that implement specific shell commands (e.g., `pwd`, `ls`, `echo`).

---

### Example Implementation

#### 1. `cmd_pkg/__init__.py`:

In this file, you can import the commands you want to expose when the user imports `cmd_pkg` as a whole.

```python
# cmd_pkg/__init__.py

from .pwd import pwd
from .ls import ls
from .echo import echo

__all__ = ['pwd', 'ls', 'echo']
```

- The `__all__` list controls what gets imported when you do `from cmd_pkg import *`.
- The `from .module import function` imports individual commands from their respective modules.

#### 2. Command Files (e.g., `pwd.py`):

Each command can be defined in its own module.

**Example for `pwd.py`**:

```python
# cmd_pkg/pwd.py

import os

def pwd():
    return os.getcwd()
```

**Example for `ls.py`**:

```python
# cmd_pkg/ls.py

import os

def ls():
    return os.listdir()
```

**Example for `echo.py`**:

```python
# cmd_pkg/echo.py

def echo(message):
    return message
```

#### 3. Main Program `shell.py`:

This is the entry point for your shell program, which can import commands from `cmd_pkg`.

```python
# shell.py

from cmd_pkg import *

def main():
    print("Running shell commands:")

    # Example usage of imported commands
    print(f"Current directory: {pwd()}")
    print(f"Directory contents: {ls()}")
    print(f"Echo: {echo('Hello, Shell!')}")

if __name__ == "__main__":
    main()
```

### How It Works:

1. **`from cmd_pkg import *`**: This imports everything listed in `__all__` in `cmd_pkg/__init__.py`, so `pwd()`, `ls()`, and `echo()` are available in `shell.py`.
2. **`from cmd_pkg import pwd`**: You can also import individual commands directly if you don't want to import everything.

### Running the Program:

When you run `shell.py`, it will execute the shell commands that were imported from `cmd_pkg`.

```bash
python shell.py
```

### Summary:

- **`cmd_pkg/`**: Contains separate modules for each shell command.
- **`__init__.py`**: Imports commands from individual modules and defines `__all__` for wildcard imports (`*`).
- **`shell.py`**: The main file where you can call the shell commands and organize the program flow.

This structure is modular and scalable, allowing you to add more commands by simply adding new modules under `cmd_pkg`.

## Dynamic Behavior

We want to dynamically load ALL the commands from `cmd_pkg` everytime we run our shell. Here's how we can achieve this:

### Dynamic Function Loading from `cmd_pkg`

1. **Use the `importlib` library**: This will allow you to dynamically import modules based on what’s available in the `cmd_pkg` directory.
2. **Use `pkgutil` or `os` to list all modules in the package**: This allows Python to inspect the `cmd_pkg` folder and find all the `.py` files.

### Code:

```python
import importlib
import pkgutil
import cmd_pkg

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

if __name__ == "__main__":
    # Load the commands dynamically from cmd_pkg
    load_commands()

    # Example usage:
    cmd = "ls"
    params = ["/usr/local/bin"]

    # Call the function dynamically from the dictionary
    if cmd in cmds:
        result = cmds[cmd](*params)
        print(result)
    else:
        print(f"Command '{cmd}' not found.")
```

### Explanation:

1. **`pkgutil.iter_modules(cmd_pkg.__path__)`**: This scans the `cmd_pkg` folder for all Python modules. It automatically finds all `.py` files (excluding `__init__.py`) and dynamically imports them.
2. **`importlib.import_module`**: Dynamically imports each module found by `pkgutil`.
3. **`dir(module)`**: This loops through all functions and attributes in the module, and `getattr` retrieves each function.
4. **`callable(obj)`**: Ensures only functions (not variables or other attributes) are added to the dictionary.

### Adding New Commands:

- Once this setup is in place, you can add any new command in the `cmd_pkg` folder (e.g., `cat.py`, `mkdir.py`), and it will automatically be picked up without modifying `shell.py`.
- Each `.py` file should contain at least one function, which will be dynamically added to the `cmds` dictionary.

### Folder Structure:

```
my_shell_project/
│
├── shell.py
├── cmd_pkg/
│   ├── __init__.py
│   ├── pwd.py
│   ├── ls.py
│   ├── echo.py
│   ├── cat.py       # New command
│   ├── mkdir.py     # New command
```

### Example:

If you add a new `cat.py` file in `cmd_pkg`:

```python
# cmd_pkg/cat.py

def cat(file):
    with open(file, 'r') as f:
        return f.read()
```

You can then use the following in `shell.py` without modifying it:

```bash
$ python shell.py
# Dynamically load and execute the cat function
cmd = "cat"
params = ["/path/to/some/file.txt"]

if cmd in cmds:
    result = cmds[cmd](*params)
    print(result)
```

### Advantages:

- **Dynamic Command Loading**: As you add more commands to `cmd_pkg`, they are automatically available without updating the main script.
- **Scalability**: The solution can scale easily as the project grows. You just need to create new `.py` files inside `cmd_pkg` with functions that represent shell commands.
