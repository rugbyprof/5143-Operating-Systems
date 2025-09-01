from os.path import isfile
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
import os
import sys
from time import sleep
from random import randint
from random import shuffle
import json

# import colorama as cr

console = Console()


def double_panel(content, inner_color="#FCB018", outer_color="#85142C"):
    inner = Panel(content, border_style=inner_color, style="white on black")
    outer = Panel(inner, border_style=outer_color, style="on black")
    return outer


def panelize(
    content,
    *,
    title=None,
    subtitle=None,
    style="white on black",
    border_style="white",
    width=None,
    markdown=False,
    syntax=None,
):
    """Prints a styled panel with text, markdown, or syntax-highlighted code.

    Args:
        content (str): The text to wrap.
        title (str): Optional panel title.
        subtitle (str): Optional bottom label.
        style (str): Style for panel text and fill.
        border_style (str): Style just for the border.
        width (int): Optional width constraint.
        markdown (bool): Interpret content as Markdown.
        syntax (str): Language name for syntax highlighting (e.g., "python").
    """
    if syntax:
        rendered = Syntax(content, syntax, line_numbers=False)
    elif markdown:
        rendered = Markdown(content)
    else:
        rendered = content

    panel = Panel(
        rendered,
        title=title,
        subtitle=subtitle,
        style=style,
        border_style=border_style,
        width=width,
    )
    console.print(panel, justify="left")


# def panelize(text, title=None, style="bold white on black"):
#   panel = Panel(text, title=title, style=style)
#   console.print(panel)

# cr.init(autoreset=True)

## 📋 Rich Style Cheat Sheet
# | Style Syntax          | Effect                        |
# | --------------------- | ----------------------------- |
# | `[bold]text[/]`       | Bold                          |
# | `[italic]text[/]`     | Italic                        |
# | `[underline]text[/]`  | Underlined                    |
# | `[strike]text[/]`     | Strikethrough                 |
# | `[dim]text[/]`        | Dimmed                        |
# | `[reverse]text[/]`    | Swapped foreground/background |
# | `[red]text[/]`        | Red foreground                |
# | `[on green]text[/]`   | Green background              |
# | `[bold red on white]` | Combo party                   |
# | `[#ff8800]text[/]`    | Hex color                     |

## 📋 TL;DR

# | Want...                      | Do This                          |
# |------------------------------|----------------------------------|
# | Markdown support             | `markdown=True`                  |
# | Syntax highlighting          | `syntax="python"` (or other lang)|
# | Width control                | `width=50`                       |
# | Just a simple box            | Pass a string and go             |

sq_let = {
    "a": "🇦",
    "b": "🇧",
    "c": "🇨",
    "d": "🇩",
    "e": "🇪",
    "f": "🇫",
    "g": "🇬",
    "h": "🇭",
    "i": "🇮",
    "j": "🇯",
    "k": "🇰",
    "l": "🇱",
    "m": "🇲",
    "n": "🇳",
    "o": "🇴",
    "p": "🇵",
    "q": "🇶",
    "r": "🇷",
    "s": "🇸",
    "t": "🇹",
    "u": "🇺",
    "v": "🇻",
    "w": "🇼",
    "x": "🇽",
    "y": "🇾",
    "z": "🇿",
}

c = ["BLUE", "CYAN", "GREEN", "MAGENTA", "RED", "WHITE", "YELLOW"]


def main(data=None, iterations=100):
    """
    Description:
        This function takes a dictionary of students and randomly selects one student from
        the pending list. After student performs task, they are moved to the finished list.
        The function continues to select students until all students are moved to the finished list.
    Input File Format:
        {
        "pending":[list of students],
        "finished":[list of students]
        }
    Args:
        data (dict): A dictionary containing key-value pairs to be displayed.
    Returns:
        None
    Raises:
        None
    """

    if not data:
        error(f"data param is empty:{data}")

    bigList = data["pending"] + data["finished"]
    print(bigList)
    sys.exit()
    # loop forever
    while 1:
        for i in range(iterations):
            os.system("clear")
            shuffle(x)
            shuffle(c)

            print(Panel(f"[bold {c[0]}]{x[0]}"))
            # print(f"{c[0]}{x[0]}")
            sleep(0.03)

        if not x[0] in y:
            break
        else:
            os.system("clear")
            print(Panel(f"[bold {c[0]}]{x[0]} [red]:cross_mark:"))
            sleep(2)


def usage():
    panelize(
        f"\n[bold #FFA500]⌘➤[/] [green]python[/] main.py [blue]fileName.json[/]",
        title="[bold red]Usage[/]",
        width=40,
    )
    sys.exit()


def error(e):
    panelize(f"[blue]{e}[/]", title="[bold red]Error![/]", width=50)
    sys.exit()


# print(Panel(f"[bold {c[0]}]{x[0]} [green]:heavy_check_mark:"))

##800080 purple

# console.print(double_panel("🎓 Ready to pass Algorithms now"),
#   justify="center")
# console_plain = Console()
# console_plain.print(" " * 80)
# print(f"[bold yellow on #800080]:{sq_let['p']}:[/]")

if __name__ == "__main__":

    if len(sys.argv) < 2:
        usage()

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        error(f"[white]File not found:[/] {filePath}")

    with open(filePath) as f:
        data = json.load(f)

    main(data)
