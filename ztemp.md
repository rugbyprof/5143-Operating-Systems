```yaml
title: Text Styling Options in Python Rich Console
library: rich
audience: CLI devs, terminal tinkerers
goal: Clarify available text styles, colors, and attributes
```

Oh yes, Terry — `rich` doesn't just do colors. It throws on a velvet robe, lights some candles, and **goes full ANSI spa day** for your terminal output. Let’s break it down:

---

## 🎨 Rich Styling: What Can You Do?

| Feature              | Supported? | How to Use It                                  |
| -------------------- | ---------- | ---------------------------------------------- |
| **Text color**       | ✅ Yes     | `[red]Hello[/red]`                             |
| **Bold**             | ✅ Yes     | `[bold]Bold text[/]`                           |
| **Italic**           | ✅ Yes     | `[italic]Slanted[/]`                           |
| **Underline**        | ✅ Yes     | `[underline]Yep[/]`                            |
| **Strikethrough**    | ✅ Yes     | `[strike]Nope[/]`                              |
| **Reverse**          | ✅ Yes     | `[reverse]Inverted[/]`                         |
| **Dimmed**           | ✅ Yes     | `[dim]Subtle[/]`                               |
| **Background color** | ✅ Yes     | `[on green]Text[/]`                            |
| **RGB / HEX colors** | ✅ Yes     | `[color(255,0,255)]Magenta![/]` or `[#FF00FF]` |
| **Named styles**     | ✅ Yes     | Combine like `[bold red on black]Warning[/]`   |

---

## 🖍️ Named Colors in Rich

Rich supports [**256 standard terminal colors**](https://rich.readthedocs.io/en/stable/appendix/colors.html#standard-colors), but here are the built-in **named** ones you can use easily:

```
black, red, green, yellow, blue, magenta, cyan, white,
bright_black, bright_red, bright_green, bright_yellow,
bright_blue, bright_magenta, bright_cyan, bright_white
```

You can use them for both foreground and background:

```python
from rich import print
print("[bold magenta on bright_black]Hello, colorful terminal![/]")
```

---

## 🧠 RGB + HEX Support

Want specific branding colors? No problem.

```python
print("[#85142C on #FCB018]MSU Maroon & Gold Baby[/]")
```

Or:

```python
print("[color(133,20,44) on color(252,176,24)]Exact same colors, RGB style[/]")
```

---

## 📋 Rich Style Cheat Sheet

| Style Syntax          | Effect                        |
| --------------------- | ----------------------------- |
| `[bold]text[/]`       | Bold                          |
| `[italic]text[/]`     | Italic                        |
| `[underline]text[/]`  | Underlined                    |
| `[strike]text[/]`     | Strikethrough                 |
| `[dim]text[/]`        | Dimmed                        |
| `[reverse]text[/]`    | Swapped foreground/background |
| `[red]text[/]`        | Red foreground                |
| `[on green]text[/]`   | Green background              |
| `[bold red on white]` | Combo party                   |
| `[#ff8800]text[/]`    | Hex color                     |

---

## 🧪 Test It Live

Here’s a quick script to test all the features:

```python
from rich.console import Console
console = Console()

console.print("[bold underline red on white] Bold Underlined Red on White [/]")
console.print("[italic dim] Italic and Dim [/]")
console.print("[reverse] Reversed! [/]")
console.print("[#FF00FF on #000000] HEX colors work too [/]")
console.print("[color(0,255,128) on color(50,50,50)] RGB syntax also works! [/]")
```

---

Want me to generate a **Rich color/style reference PDF** for your students or a little terminal-based color tester app? I can bling it out.


```yaml
title: Advanced Panel Function with Markdown, Syntax, and Sizing
library: rich
goal: Create a panel wrapper for styled, optionally sized output
audience: CLI app builders, educators, stylish terminal nerds
```

Yes yes YES, Terry — you can absolutely size `rich` panels *and* fill them with **Markdown** or **syntax-highlighted code**. Let’s build you a **superpowered panel function** that handles:

- ✅ plain text  
- ✅ rich Markdown  
- ✅ syntax-highlighted code  
- ✅ optional width control  
- ✅ optional border + text styles  

---

## 🧠 The Super `panelize()` Function

```python
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax

console = Console()

def panelize(
    content,
    *,
    title=None,
    subtitle=None,
    style="white on dark_blue",
    border_style=None,
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
        rendered = Syntax(content, syntax, line_numbers=True)
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
    console.print(panel)
```

---

## 🧪 Examples

### ✅ Basic Box

```python
panelize("This is boxed in glory.")
```

### 📖 Markdown Panel

```python
panelize(
    "# Welcome\nThis is **bold**, this is *italic*.",
    title="Markdown Panel",
    markdown=True,
    style="white on blue",
)
```

### 🧠 Syntax Highlighted Code

```python
code = '''
def greet(name):
    return f"Hello, {name}!"
'''

panelize(code, title="Python Snippet", syntax="python", width=60)
```

### 🎯 Sizing Panels

- Use `width=NN` to **hard-limit the panel width**
- Panel will auto-wrap text to fit inside
- Width can go as wide as your terminal, obviously

---

## 📋 TL;DR

| Want...                      | Do This                          |
|------------------------------|----------------------------------|
| Markdown support             | `markdown=True`                  |
| Syntax highlighting          | `syntax="python"` (or other lang)|
| Width control                | `width=50`                       |
| Just a simple box            | Pass a string and go             |

---

Would you like this turned into a **module you can import**, or a CLI tool like `py-panel` so your students can box their notes/code from the terminal? I can package it up!