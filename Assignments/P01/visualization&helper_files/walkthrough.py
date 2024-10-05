"""
This script demonstrates how to use the rich library to create a simple
command-line interface for a file system. The script simulates the
standard usage of the `ls`, `mkdir`, `cd`, `cp`, `rm`, and `pwd` commands.

It also pauses for a few seconds to since this is meant as a demonstration
and not a real-time simulation.

"""

import time
from rich import print
from rich.table import Table
from rich.box import SIMPLE
import time
from rich.progress import track


def display_ls(files):
    table = Table(
        show_header=True,
        header_style="bold blue",
    )  # box=SIMPLE
    table.add_column("Filename", style="dim", width=20)
    table.add_column("Owner", width=10)
    table.add_column("Permissions", width=10)
    table.add_column("Size", justify="right")
    for filename, (owner, perms, size) in files.items():
        table.add_row(filename, owner, perms, size)
    print(table)

    for i in track(range(5), description="Processing..."):
        time.sleep(0.5)  # Simulate work being done


def display_pwd(directory):
    print(f"[bold cyan]Current Directory:[/bold cyan] [green]{directory}[/green]")
    for i in track(range(5), description="Processing..."):
        time.sleep(0.5)  # Simulate work being done


# Dummy data for the example
current_directory = "/home/user"
files_before = {
    "file1.txt": ("user", "-rw-r--r--", "12 KB"),
    "file2.txt": ("user", "-rw-r--r--", "15 KB"),
    "file3.txt": ("user", "-rw-r--r--", "18 KB"),
    "file4.txt": ("user", "-rw-r--r--", "14 KB"),
    "file5.txt": ("user", "-rw-r--r--", "13 KB"),
    "file6.txt": ("user", "-rw-r--r--", "16 KB"),
    "file7.txt": ("user", "-rw-r--r--", "11 KB"),
    "project": ("user", "drwxr-xr-x", "[Dir]"),
}
files_after = {
    "file3.txt": ("user", "-rw-r--r--", "18 KB"),
    "file4.txt": ("user", "-rw-r--r--", "14 KB"),
    "file6.txt": ("user", "-rw-r--r--", "16 KB"),
    "file7.txt": ("user", "-rw-r--r--", "11 KB"),
    "project": ("user", "drwxr-xr-x", "[Dir]"),
    "newfolder": ("user", "drwxr-xr-x", "[Dir]"),
}

# Demonstrate the commands
print("[bold blue]Command:[/bold blue] [green]ls[/green]")
display_ls(files_before)

print("\n[bold blue]Command:[/bold blue] [green]mkdir newfolder[/green]")
print("[bold green]Folder 'newfolder' created.[/bold green]")
for i in track(range(5), description="Processing..."):
    time.sleep(0.5)  # Simulate work being done

print("\n[bold blue]Command:[/bold blue] [green]ls[/green]")
display_ls(files_after)

print("\n[bold blue]Command:[/bold blue] [green]cd newfolder[/green]")
current_directory += "/newfolder"
display_pwd(current_directory)

print("\n[bold blue]Command:[/bold blue] [green]cp ../file1.txt .[/green]")
print("[bold green]File 'file1.txt' copied to current directory.[/bold green]")
for i in track(range(5), description="Processing..."):
    time.sleep(0.5)  # Simulate work being done


print(
    "\n[bold blue]Command:[/bold blue] [green]rm ../file1.txt ../file2.txt ../file5.txt[/green]"
)
print(
    "[bold green]Files 'file1.txt', 'file2.txt', and 'file5.txt' removed.[/bold green]"
)
for i in track(range(5), description="Processing..."):
    time.sleep(0.5)  # Simulate work being done

print("\n[bold blue]Command:[/bold blue] [green]ls[/green]")
display_ls(files_after)

print("\n[bold blue]Command:[/bold blue] [green]pwd[/green]")
display_pwd(current_directory)
