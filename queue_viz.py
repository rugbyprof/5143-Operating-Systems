from rich import print
from rich.table import Table
from rich.live import Live
import random
import time
from rich.progress import SpinnerColumn
from rich.console import Console

# Gets the width of the console so I can size each column as a percentage so
# the width stays static looking and the "processes" can grow and shrink.
console = Console()
terminal_width = console.width

STAGES = ["New", "Ready", "Running", "Exit"]

jobs = []
pid_counter = 1


def create_job():
    global pid_counter
    job = {
        "pid": pid_counter,
        "burst": random.randint(2, 5),  # CPU burst time
        "stage": 0,  # start at "New"
    }
    pid_counter += 1
    return job


def get_num():
    """Helper for make row"""
    return random.randint(1, 99)


def get_proc():
    """Helper for make row"""
    return f"P{random.randint(1,50)}"


def make_row(queueName):
    """This function builds a row with 2 columns. The queue name on the left, and a random number of processes on the right."""

    processes = ""
    for job in jobs:
        if STAGES[job["stage"]] == queueName:
            # processes += str(f"[on green][bold][[/bold][red]{get_proc()}[/red] {get_num()}[bold]][/bold][/on green] ")
            processes += str(
                f"[bold][[/bold][bold blue]{job['pid']} {job['burst']}[/bold blue][bold]][/bold]"
            )
    return [queueName, processes]


def generate_table() -> Table:
    """
    - This function returns a `rich` table that displays all the queue contents. How you format that is up to you.
    - The `end_section=True` is what puts a line between rows
    - I left a commented line to show how you can change background colors, but is not the whole table or column or row. You'll see.
    - All I do is call `make_row` with the queue name and my random ranges. The "*" is how you add a "list" as a row, it explodes it basically,
       and since `make_row` returns a list with one entry per column, we need to expand it.
    - You will probably have to pass in your queues or put this in a class to generate your own table .... or don't.
    """
    # Create the table
    table = Table(show_header=True)
    # table.add_column("Queue", style="bold yellow on blue dim", width=int(terminal_width*.1))
    table.add_column("Queue", style="bold red", width=int(terminal_width * 0.1))
    table.add_column("Processes", width=int(terminal_width * 0.9))
    table.add_row(*make_row("New"), end_section=True)
    table.add_row(*make_row("Ready"), end_section=True)
    table.add_row(*make_row("Running"), end_section=True)
    # table.add_row(*make_row("Peripheral"), end_section=True)
    table.add_row(*make_row("Exit"), end_section=True)
    return table


"""
This is how "rich" looks like its animated. The `Live` method keeps calling
the `generate_table()` function 40 times in this case with a small sleep in
between. I haven't experimented with the refresh_per_second value, so I don't know.
"""
with Live(generate_table(), refresh_per_second=4) as live:
    # Main loop
    for tick in range(40):
        # Randomly add new jobs
        if random.random() < 0.3:
            jobs.append(create_job())

        # Process jobs
        for job in list(jobs):  # copy so we can modify
            if job["stage"] == 2:  # Running
                job["burst"] -= 1
                if job["burst"] <= 0:
                    job["stage"] = 3  # Move to Exit
            elif job["stage"] < 2:  # New → Ready → Running
                # small chance to advance stage
                if random.random() < 0.5:
                    job["stage"] += 1

        # Remove jobs in Exit after a while
        # jobs = [j for j in jobs if j["stage"] < 3 or random.random() < 0.9]

        live.update(generate_table())
        time.sleep(0.5)