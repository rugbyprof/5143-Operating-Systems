import glob 
from functions.add import Add
from functions.sub import Sub

# from functions import *



command = "ls -lr Dropbox > foo"
parts = command.split()
print(parts)
for part in parts:
    if '-' in part:
        print(f"flags: {part}")


files = glob.glob("*.*")
print(files)

print(Add(9,9))