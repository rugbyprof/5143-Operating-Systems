"""
1st way is to import the function from the file that generates the inputs 
for our simulation, then call it with whatever params you see fit.
"""
from generate_input import generate_file


def prep_simulation():
    """This function calls the generate file method and can open the
    file that the results were written to, or get them directly from
    "results" below.
    """
    params = {
        "ofile": "filename.wut",
        "nj": 1000,
        "minCpuBT": 5,
        "maxCpuBT": 15,
        "minIOBT": 10,
        "maxIOBT": 20,
    }
    results = generate_file(**params)
    print(results)


if __name__ == "__main__":
    prep_simulation()
