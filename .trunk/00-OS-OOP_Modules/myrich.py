#!/usr/local/bin/python3
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
from rich.table import Table
from rich.panel import Panel

# from rich.console import render_group
import random
import json
import sys, os


console = Console()
layout = Layout()

layout.split_column(Layout(name="upper", ratio=1), Layout(name="lower", ratio=2))

layout["upper"].split_row(
    Layout(name="CPU"),
    Layout(name="REGISTERS"),
    Layout(name="ALU"),
)

layout["lower"].split_row(
    Layout(name="Processes", ratio=1),
    Layout(name="Memory", ratio=2),
)


class MyLayout:
    def __init__(self):
        pass


class MyProgressBar:
    def __init__(self, **kwargs):
        self.min = kwargs.get("min", 3)
        self.max = kwargs.get("max", 30)
        self.size = random.randint(self.min, self.max)
        self.title = kwargs.get("title", "Buffer")
        self.foreColor = kwargs.get("foreColor", "green")
        self.backColor = kwargs.get("backColor", "#00FF00")
        self.bar = ""

    def generate_buffer(self):
        self.bar = ""
        adjust = random.randint(-4, 4)
        for i in range(self.size + adjust):
            self.bar += " "

    def __rich__(self) -> Panel:
        self.generate_buffer()
        return Panel(
            f"[{self.foreColor} on {self.backColor}]{self.bar}", title=self.title
        )


class MyText:
    """Renders the time in the center of the screen."""

    def __init__(self, **kwargs):
        self.txt = kwargs.get("txt", "text")
        self.style = kwargs.get("style", "")  # bold , italics
        self.color = kwargs.get("color", "blue")
        self.justify = kwargs.get("justify", "center")  # center , left, right

    # def __rich__(self) -> Text:
    #     return Text(datetime.now().ctime(), style="bold magenta", justify="center")

    def __rich__(self) -> Text:
        return Text(self.txt, style=self.style + " " + self.color, justify=self.justify)


class Buffer:
    def __init__(self, min=3, max=30):
        self.min = min
        self.max = max
        self.size = random.randint(self.min, self.max)
        self.bar = ""

    def generate_buffer(self):
        self.bar = ""
        adjust = random.randint(-4, 4)
        for i in range(self.size + adjust):
            self.bar += " "

    def __rich__(self) -> Panel:
        self.generate_buffer()
        return Panel(f"[green on #00FF00]{self.bar}", title="Buffer")


class Clock:
    """Renders the time in the center of the screen."""

    def __rich__(self) -> Text:
        return Text(datetime.now().ctime(), style="bold magenta", justify="center")


class MyTable:
    """returns a table in a rich panel."""

    def __init__(self, **kwargs):

        self.title = kwargs.get("title", "Table Title")
        self.style = kwargs.get("style", "white")
        self.justify = kwargs.get("justify", "left")
        self.no_wrap = kwargs.get("no_wrap", True)

        self.table = Table(title=self.title)
        self.numCols = 0
        self.numRows = 0

    def addColumn(self, **kwargs):
        col_head = kwargs.get("col_head", "")
        style = kwargs.get("style", self.style)
        justify = kwargs.get("justify", self.justify)  # left right center
        no_wrap = kwargs.get("no_wrap", self.no_wrap)
        self.table.add_column(col_head, justify=justify, style=style, no_wrap=no_wrap)
        self.numCols += 1

    def addRow(self, row):
        if len(row) != self.numCols:
            print("error: row doesn't match cols in table!")
            sys.exit()
        print(*row)
        self.table.add_row(*row)
        self.numRows += 1

    def rows(self):
        self.numRows

    def cols(self):
        self.numCols

    def __rich__(self) -> Panel:

        return Panel(self.table)


if __name__ == "__main__":
    T = MyTable()

    T.addColumn(col_head="one")
    T.addColumn(col_head="two")
    T.addColumn(col_head="three")

    T.addRow(["booty", "call", "hello"])
    T.addRow(["slpooy", "big", "whale"])
    T.addRow(["no", "body", "baby"])

    layout["Memory"].update(T)
    with Live(layout, screen=True, redirect_stderr=False) as live:
        try:
            while True:
                sleep(0)
        except KeyboardInterrupt:
            pass
