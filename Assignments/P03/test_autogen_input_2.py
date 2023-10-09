"""
The 2nd way is to use something like the the `subprocess` library which 
lets us run shell commands from our python script
"""
import os


def prep_simulation():
    """This function calls the `generate_input.py` like its a command
    in the shell.
    """

    file = "generate_input.py"
    params = "ofile=filename.wut nj=1000 minCpuBT=5 maxCpuBT=15 minIOBT=10 maxIOBT=20"
    results = os.system(f"python3  {file} {params}")

    print(results)


if __name__ == "__main__":
    prep_simulation()
