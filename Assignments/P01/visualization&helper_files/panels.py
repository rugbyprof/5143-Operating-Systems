"""
This script demonstrates how to use the rich library to create a simple
command-line interface for a file system. The script simulates the
standard usage of the `ls`, `mkdir`, `cd`, `cp`, `rm`, and `pwd` commands.

It also pauses for a few seconds to since this is meant as a demonstration
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

Console().clear()

"""
COULD BE DONE PROGRAMATICALLY AFTER SELECTING FROM TABLE IN SqlIte
"""
table = Table(show_header=True, header_style="bold cyan")
table.add_column("permissions", style="bold")
table.add_column("block", style="bold")
table.add_column("owner", style="bold")
table.add_column("group", style="bold")
table.add_column("size", style="bold")
table.add_column("date", style="bold")
table.add_column("name", style="bold")

table.add_row(
    "-rw-r--r--@", "1", "griffin", "staff", "3.0K", "Nov 17 2022", "cartridge.sql"
)
table.add_row("-rw-r--r--", "1", "griffin", "staff", "173B", "Oct 18 2022", "catlan.py")
table.add_row(
    "-rw-r--r--@", "1", "griffin", "staff", "18M", "Nov 17 2022", "cp_three.pdf"
)
table.add_row(
    "-rw-r--r--@", "1", "griffin", "staff", "11K", "Jul 10 2023", "github.css"
)
table.add_row("drwxr-xr-x", "7", "griffin", "staff", "224B", "Oct 3 2023", "go/")
table.add_row(
    "-rw-r--r--@", "1", "griffin", "staff", "4.9K", "Nov 3 2022", "griffin.zsh-theme"
)
table.add_row(
    "-rwxr-xr-x", "1", "griffin", "staff", "430B", "Nov 12 2022", "hashtest.py"
)
table.add_row(
    "----------",
    "1",
    "griffin",
    "staff",
    "10M",
    "Nov 23 2022",
    "logfile",
    style="bold green on blue",
)
table.add_row("-rw-r--r--@", "1", "griffin", "staff", "162B", "Oct 10 2022", "missile")
table.add_row(
    "-rw-r--r--", "1", "griffin", "staff", "303B", "Nov 13 2022", "officeStuff.txy"
)
table.add_row("-rw-r--r--@", "1", "griffin", "staff", "1.4K", "Nov 29 2022", "ship")
table.add_row(
    "-rw-r--r--@", "1", "griffin", "staff", "6.0K", "Nov 24 2022", "stats.csv"
)
table.add_row("drwxr-xr-x", "4", "griffin", "staff", "128B", "Sep 25 2023", "tmp/")
table.add_row(
    "-rw-r--r--@", "1", "griffin", "staff", "1.7K", "Nov 17 2022", "torpedo.sql"
)
table.add_row("drwxr-xr-x", "3", "griffin", "staff", "96B", "Sep 5 2023", "ztemp/")


text = Text()
text.append("$: ", style="bold green")
text.append("chmod 000 logfile", style="bold white")


# Create a top panel for the Linux command output
top_panel = Panel(
    text, title="Linux Command", border_style="blue", style="bold", title_align="left"
)

# Create a bottom panel for the fake listing data
bottom_panel = Panel(
    table,
    title="Output:",
    border_style="green",
    style="bold",
    highlight="red",
    title_align="left",
)

# Create a console and specify the screen height
console = Console(height=50)  # Adjust the height as needed

# Print the top panel with a divider and the bottom panel
console.print(top_panel)
console.print(bottom_panel)
