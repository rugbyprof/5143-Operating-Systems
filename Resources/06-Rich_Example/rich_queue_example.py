# from rich import print
# from rich.table import Table
# import random


# def get_num():
#     return random.randint(1,99)

# def get_proc():
#     return f"P{random.randint(1,50)}"


# def make_row(queueName,a=2,b=5):
#     num_processes = random.randint(a, b)
#     processes = ""
#     for _ in range(num_processes):
#         processes += str(f"[on green][bold][[/bold][red]{get_proc()}[/red] {get_num()}[bold]][/bold][/on green] ")
#     return [queueName,processes]

# # Create the table
# table = Table(show_header=False)
# table.add_column("Queue", style="bold yellow on blue")
# table.add_column("Processes")


# table.add_row(*make_row("New",3,7),end_section=True)
# table.add_row(*make_row("Ready",2,4),end_section=True)
# table.add_row(*make_row("Running",1,3),end_section=True)
# table.add_row(*make_row("Peripheral",1,2),end_section=True)
# table.add_row(*make_row("Exit",7,15),end_section=True)

# print(table)

from rich import print
from rich.table import Table
from rich.live import Live
import random
import time
from rich.progress import SpinnerColumn
from rich.console import Console

console = Console()
terminal_width = console.width



def get_num():
    return random.randint(1,99)

def get_proc():
    return f"P{random.randint(1,50)}"

def make_row(queueName, a=2, b=5):
    num_processes = random.randint(a, b)
    processes = ""
    for _ in range(num_processes):
        #processes += str(f"[on green][bold][[/bold][red]{get_proc()}[/red] {get_num()}[bold]][/bold][/on green] ")
        processes += str(f"[bold][[/bold][bold blue]{get_proc()} {get_num()}[/bold blue][bold]][/bold]")
    return [queueName, processes]

def generate_table() -> Table:
    # Create the table
    table = Table(show_header=False)
    #table.add_column("Queue", style="bold yellow on blue dim", width=int(terminal_width*.1))
    table.add_column("Queue", style="bold red", width=int(terminal_width*.1))
    table.add_column("Processes", width=int(terminal_width*.9))
    table.add_row(*make_row("New", 3, 7), end_section=True)
    table.add_row(*make_row("Ready", 2, 4), end_section=True)
    table.add_row(*make_row("Running", 1, 3), end_section=True)
    table.add_row(*make_row("Peripheral", 1, 2), end_section=True)
    table.add_row(*make_row("Exit", 7, 10), end_section=True)
    return table


with Live(generate_table(), refresh_per_second=4) as live:
    for _ in range(40):
        time.sleep(0.4)
        live.update(generate_table())



# with Live(table, refresh_per_second=4) as live:
#     try:
#         while True:
#             table.rows.clear()  # clear previous rows
            

#             live.update(table)  # update the live display
#             time.sleep(1)
#             with live.status(SpinnerColumn()):
#                 pass
#     except KeyboardInterrupt:
#         print("\nSimulation stopped by user.")
