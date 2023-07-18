"""
Demonstrates a dynamic Layout
"""

from datetime import datetime

from time import sleep

from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.text import Text


class coolConsole(object):
    def __init__(self):
        self.console = Console()
        self.layout = Layout()

        self.layout.split(
            Layout(name="header", size=1),
            Layout(ratio=1, name="main"),
            Layout(size=10, name="footer"),
        )

        self.layout["main"].split(
            Layout(name="side"), Layout(name="body", ratio=2), direction="horizontal"
        )

        self.layout["side"].split(Layout(), Layout())

        self.layout["body"].update(
            Align.center(
                Text(
                    """This is a demonstration of rich.Layout\n\nHit Ctrl+C to exit""",
                    justify="center",
                ),
                vertical="middle",
            )
        )


class Clock:
    """Renders the time in the center of the screen."""

    def __rich__(self) -> Text:
        return Text(datetime.now().ctime(), style="bold magenta", justify="center")




if __name__=='__main__':
    cc = coolConsole()
    cc.layout["header"].update(Clock())

    with Live(cc.layout, screen=True, redirect_stderr=False) as live:
        try:
            while True:
                sleep(1)
        except KeyboardInterrupt:
            pass