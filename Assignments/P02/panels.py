from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.style import Style

highlighted_style = "on yellow"

# Function to execute a Linux command and return the output
def execute_linux_command(command):
    import subprocess
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        return output
    except subprocess.CalledProcessError as e:
        return str(e)

# # Create a table for fake listing data
# table = Table(show_header=True, header_style="bold cyan")
# table.add_column("Name", style="bold")
# table.add_column("Size", style="bold")
# table.add_column("Modified", style="bold")

# # Add fake listing data rows to the table
# table.add_row("file1.txt", "100KB", "2023-10-16 10:30 AM")
# table.add_row("file2.txt", "50KB", "2023-10-15 02:45 PM")
# table.add_row("dir1", "-", "2023-10-14 11:15 AM")
# table.add_row("file3.txt", "75KB", "2023-10-14 09:00 AM")
# table.add_row("dir2", "-", "2023-10-13 03:20 PM")

table = Table(show_header=True, header_style="bold cyan")
table.add_column("permissions", style="bold")
table.add_column("block", style="bold")
table.add_column("owner", style="bold")
table.add_column("group", style="bold")
table.add_column("size", style="bold")
table.add_column("date", style="bold")
table.add_column("name", style="bold")

table.add_row("-rw-r--r--@","1","griffin","staff","3.0K","Nov 17 2022","cartridge.sql")
table.add_row("-rw-r--r--","1","griffin","staff","173B","Oct 18 2022","catlan.py")
table.add_row("-rw-r--r--@","1","griffin","staff","18M","Nov 17 2022","cp_three.pdf")
table.add_row("-rw-r--r--@","1","griffin","staff","11K","Jul 10 2023","github.css")
table.add_row("drwxr-xr-x","7","griffin","staff","224B","Oct 3 2023","go/")
table.add_row("-rw-r--r--@","1","griffin","staff","4.9K","Nov 3 2022","griffin.zsh-theme")
table.add_row("-rwxr-xr-x","1","griffin","staff","430B","Nov 12 2022","hashtest.py")
table.add_row("----------","1","griffin","staff","10M","Nov 23 2022","logfile",style="bold green on blue")
table.add_row("-rw-r--r--@","1","griffin","staff","162B","Oct 10 2022","missile")
table.add_row("-rw-r--r--","1","griffin","staff","303B","Nov 13 2022","officeStuff.txy")
table.add_row("-rw-r--r--@","1","griffin","staff","1.4K","Nov 29 2022","ship")
table.add_row("-rw-r--r--@","1","griffin","staff","6.0K","Nov 24 2022","stats.csv")
table.add_row("drwxr-xr-x","4","griffin","staff","128B","Sep 25 2023","tmp/")
table.add_row("-rw-r--r--@","1","griffin","staff","1.7K","Nov 17 2022","torpedo.sql")
table.add_row("drwxr-xr-x","3","griffin","staff","96B","Sep 5 2023","ztemp/")





# Create a top panel for the Linux command output
top_panel = Panel("$: chmod 000 logfile", title="Linux Command", border_style="blue", style="bold")

# Create a bottom panel for the fake listing data
bottom_panel = Panel(table, title="Output:", border_style="green", style="bold", highlight="red")

# Create a console and specify the screen height
console = Console(height=30)  # Adjust the height as needed

# Print the top panel with a divider and the bottom panel
console.print(top_panel)
console.print(bottom_panel)

