## Fast Api - Backend for Filesystem

## Resources

### Fast Api Tutorial and Docs

- Remember that they run the api differently using `uvicorn` from the command line and we
  use `python filename.py` which invokes `uvicorn` from the `__main__` block inside the file.
- https://fastapi.tiangolo.com/tutorial/

### Realpython tutorial

- Realpython is usually very good.
- https://realpython.com/fastapi-python-web-apis/

### Requirements

- You can install the `requirements.txt` by running: `python -m pip install -r requirements.txt`
- Remember that I decided to use Pythons `Vertualenv` instead of conda. So I think this command should work for anyone using `conda` as thier environment: `conda install --file requirements.txt`
-

## Api Methods

### GET

- `/id/?name=[str]&pid=[int]`
  - gets the id for a particular item based on `{name}` and the `{pid}` (parent id)
  - **REQUIRED**:
    - name [str] : name of item
    - pid [int] : parent id of item
  - **RETURNS `[int]` id for a file or directory**
- `/ls/`
  - does a directory listing
  - **RETURNS `[str]`(listing)**
- `/cd/?did=n`
  - Changes from one directory to a another
  - **REQUIRED**:
    - did [int] = the directory `{id}` to change to.
  - **RETURNS**
    - `[bool]` (command was successful)
  - **EXAMPLE**
    - If a user types in `cd ../folder1/subfolder1/` you need to parse this statement and find the id for `subfolder` based on its location in `folder1` based its location one folder back from current location.
- `/grep/?input=[str] | id=[int] & pattern`[str]
  - **REQUIRED**:
    - One of the following parameters is required OR both can be used:
      - `input` (string): The input as a string.
      - `id` (list): List of input files (e.g. [23] | [22,11,43])
    - `pattern` (str): pattern to match in the files or string.
  - **OPTIONAL**
    - flags [list] = list of flags (e.g. [l,i,c])
  - **RETURNS** `[str]` (output of grep command)
- `/wc/?input=[str] OR id=[int] or flags=[list]`
  - **REQUIRED**:
    - One of the following parameters is required:
      - `input` (string): The input as a string.
      - `id` (int): The input as an ID.
  - **OPTIONAL**
    - flags [list] = list of flags (e.g. [L,c,l,m])
  - **RETURNS** `[str]` (output of wc command based on flags)
- `/history/`
  - **RETURNS** `[list]` list of commands from oldest to newest
- `/sort/?id=[int] | input=[str]`
  - **REQUIRED**:
    - One of the following parameters is required OR both can be used:
      - `input` (string): The input as a string.
      - `id` (list): List of input files (e.g. [23] | [22,11,43])
- `/less/?input=[str] | id=[int]`
  - **REQUIRED**:
    - One of the following parameters is required OR both can be used:
      - `input` (string): The input as a string.
      - `id` (list): List of input files (e.g. [23] | [22,11,43])
  - **OPTIONAL**
    - flags [list] = list of flags (e.g. [])
  - **RETURNS** `[str]` (output of grep command)
- `/head/?input=[str] | id=[int]`
  - **REQUIRED**:
    - One of the following parameters is required OR both can be used:
      - `input` (string): The input as a string.
      - `id` (list): List of input files (e.g. [23] | [22,11,43])
  - **OPTIONAL**
    - flags [list] = list of flags (e.g. [n])
  - **RETURNS** `[str]` (output of grep command)
- `/tail/?input=[str] | id=[int]`
  - **REQUIRED**:
    - One of the following parameters is required OR both can be used:
      - `input` (string): The input as a string.
      - `id` (list): List of input files (e.g. [23] | [22,11,43])
  - **OPTIONAL**
    - flags [list] = list of flags (e.g. [n])
  - **RETURNS** `[str]` (output of grep command)
- `/pwd/?id=[int]`
  - Continuosly select parent id until you get to the root, then print

### PUT

- `/rm/?id=[int]&flags=[list]`
  - **REQUIRED**:
    - id [int] = id or a file or directory
  - **OPTIONAL**:
    - flags [list] = list of flags (e.g. [r,f])
  - **RETURNS** `[bool]` (command was successful)
- `/mv/?from=[int]&to=[int]&new_name=[str]`
  - **REQUIRED**:
    - from [int] = id of item to be moved
    - fo [int] = id of folder to be moved to
  - **OPTIONAL**:
    - new_name [str] = a string in wich to rename the item being moved
  - **RETURNS** `[bool]` (command was successful)
- `/cp/?from=[int]&to=[int]&new_name[str]`
  - **REQUIRED**:
    - from [int] = id of item to be moved
    - fo [int] = id of folder to be moved to
    - new_name [str] = a string in wich to rename the item being moved
  - **RETURNS** `[bool]` (command was successful)
- `/chmod/?`

### POST

- `/mkdir/?pid=[int]`
  - **REQUIRED**:
    - pid [int] = parent id
    - name [str] = name of directory
  - **RETURNS** `[bool]` (command was successful)
