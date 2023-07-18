#!/usr/local/bin/python3

import time
from time import sleep
import random
from rich import print
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
from rich.layout import Layout
from rich.text import Text

layout = Layout()

class Clock:
    """Renders the time in the center of the screen."""

    def __rich__(self) -> Text:
        return Text(datetime.now().ctime(), style="bold magenta", justify="center")



def generate_buffer(size=10) -> Panel:
    out = ""
    for i in range(size):
        out += ' '
    return Panel(f'[green on #00FF00]{out}', title="Buffer")


def client_panel(info) -> Panel:
    return Panel(f'[green on #00FF00]{info}', title="Client")

if __name__=='__main__':
    
    layout.split(
        Layout(name="header", size=1),
        Layout(ratio=1, name="main"),
        Layout(size=10, name="footer"),
    )

    layout["main"].split(
        Layout(name="side"), Layout(name="body", ratio=2)#, direction="horizontal"
    )

    layout["side"].split(Layout(), Layout())

    

    i = 10
    info = {'id':"client 1","stock":"goog","price":555.68}

    layout["side"].update(Clock())

    # with Live(generate_buffer(), refresh_per_second=4) as live:
    with Live(layout, screen=True, redirect_stderr=False) as live:
        try:
            while True:
                sleep(1)
                
        except KeyboardInterrupt:
            pass