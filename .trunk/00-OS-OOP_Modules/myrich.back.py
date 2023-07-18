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


stock_data = []

with open("stocks.json") as f:
    data = f.read()
    stock_data = json.loads(data)

console = Console()
layout = Layout()

layout.split(
    Layout(name="header", size=1),
    Layout(name="main"),
    Layout(size=3, name="footer"),
)

layout["main"].split(
    Layout(name="left"),
    Layout(name="center"),
    Layout(name="right"),
    # direction="horizontal"
)

layout["left"].ratio = 1
layout["center"].ratio = 1
layout["right"].ratio = 1


def random_price(min=3, max=1000):
    price = random.randint(3, 1000)
    price *= random.random()
    price = round(price, 2)
    if price < 10:
        price = "000" + str(price)
    elif price < 100:
        price = "00" + str(price)
    elif price < 1000:
        price = "0" + str(price)

    if len(price) < 7:
        price = price + "0"
    return price


def make_producers(min=1, max=20):
    num = random.randint(min, max)
    results = []
    for i in range(num):
        sid = i
        if sid < 10:
            sid = str(0) + str(i)
        random.shuffle(stock_data)
        results.append(
            {"id": "P" + str(sid), "stock": stock_data[0][:4], "price": random_price()}
        )
    random.shuffle(results)
    return results


def make_consumers(min=1, max=20):
    num = random.randint(min, max)
    results = []
    for i in range(num):
        sid = i
        if sid < 10:
            sid = str(0) + str(i)
        random.shuffle(stock_data)
        results.append(
            {"id": "P" + str(sid), "stock": stock_data[0][:4], "price": random_price()}
        )
    random.shuffle(results)
    return results


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


class Producers:
    """Renders the time in the center of the screen."""

    def __init__(self):
        self.producer_info = []

    def build_table(self):
        temp = ["🍝", "🌮", "🌭", "🍔"]
        bonus = [":spaghetti:", ":taco:", ":hot_dog:", ":hamburger:"]
        self.producer_info = make_producers()
        table = Table(title="Producers")
        table.add_column("Id", justify="center", style="cyan", no_wrap=True)
        table.add_column("Stock", style="magenta")
        table.add_column("Price", justify="right", style="green")
        table.add_column("Bonus", justify="right", style="green")

        for client in self.producer_info:
            b = random.randint(0, len(bonus) - 1)
            table.add_row(
                str(client["id"]), str(client["stock"]), str(client["price"]), bonus[b]
            )

        return table

    def count(self):
        return str(len(self.producer_info))

    def __rich__(self) -> Panel:

        return Panel(self.build_table())


class Consumers:
    """Renders the time in the center of the screen."""

    def __init__(self):
        self.consumer_info = []

    def build_table(self):
        self.consumer_info = make_consumers()
        table = Table(title="Consumers")
        table.add_column("Id", justify="center", style="cyan", no_wrap=True)
        table.add_column("Stock", style="blue")
        table.add_column("Price", justify="right", style="red")

        for client in self.consumer_info:
            table.add_row(str(client["id"]), str(client["stock"]), str(client["price"]))

        return table

    def count(self):
        return str(len(self.consumer_info))

    def __rich__(self) -> Panel:
        return Panel(self.build_table())


class Counts:
    """Renders the time in the center of the screen."""

    def __init__(self, P, C):
        self.p = P
        self.c = C

    def build_table(self):
        self.client_info = make_consumers()
        table = Table(title="Counts")
        table.add_column("Producers", justify="center", style="cyan", no_wrap=True)
        table.add_column("Consumers", justify="center", style="green", no_wrap=True)
        table.add_row(self.p.count(), self.c.count())

        return table

    def __rich__(self) -> Panel:
        return Panel(self.build_table())


class Processes:
    """Renders the time in the center of the screen."""

    def __init__(self, p):
        self.processes = p

    def build_table(self):
        self.client_info = make_consumers()
        table = Table(title="Processes")
        table.add_column("Id's", justify="center", style="cyan", no_wrap=True)
        for p in self.processes:
            table.add_row(p)

        return table

    def __rich__(self) -> Panel:
        return Panel(self.build_table())


if __name__ == "__main__":
    K = Clock()
    P = Producers()
    C = Consumers()
    B = Buffer()
    S = Counts(P, C)
    layout["header"].update(K)
    layout["left"].update(P)
    layout["center"].update(S)
    layout["right"].update(C)
    layout["footer"].update(B)

    with Live(layout, screen=True, redirect_stderr=False) as live:
        try:
            while True:
                sleep(0)
        except KeyboardInterrupt:
            pass
