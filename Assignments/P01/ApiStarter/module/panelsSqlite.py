

import sqlite3
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from shell import runShell

# Connect to the SQLite database
def get_filesystem_data(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Select all the file system info from the database
    cursor.execute("SELECT * FROM files")
    data = cursor.fetchall()

    cursor.execute(f"PRAGMA table_info({"files"});")
    results = cursor.fetchall()
    fields = [result[1] for result in results]
    conn.close()

    return [fields] + data

#style="bold green on blue",

# Function to display file system using Rich
def display_filesystem(data,idx=0):
    # Initialize the Rich table
    table = Table(show_header=True, header_style="bold cyan")
    
    # Add columns headers to the table
    for field in data[0]:
        table.add_column(field, style="bold")
    data = data[1:]

    # Populate the table with data from the database
    i = 0
    for row in data:
        row = [str(cell) for cell in row]
        if i == idx:
            table.add_row(*row, style="bold green on blue")
        else:
            table.add_row(*row)
        i += 1

    # Text command at the top (just for demonstration)
    text = Text()
    text.append("$: ", style="bold green")
    text.append("chmod 000 logfile", style="bold white")

    # Create the top panel for the command
    top_panel = Panel(
        text,
        title="Linux Command",
        border_style="blue",
        style="bold",
        title_align="left",
    )

    # Create the bottom panel for the directory listing
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

    # Print the panels
    # console.print(top_panel)
    console.print(bottom_panel)


# Path to your SQLite database
db_path = "../data/filesystem.db"

# Retrieve data from the database
filesystem_data = get_filesystem_data(db_path)

#print(filesystem_data)


# Display the data in the Rich table
display_filesystem(filesystem_data)

runShell(display_filesystem,filesystem_data)
