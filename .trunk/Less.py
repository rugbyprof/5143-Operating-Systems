from getch import Getch

getch = Getch()


def callGetch():
    print(getNext())


def getNext():

    char = getch()  # read a character (but don't print)

    if char == "\x03":  # ctrl-c
        raise SystemExit("Bye.")

    elif char in "\x1b":  # arrow key pressed
        null = getch()  # waste a character
        direction = getch()  # grab the direction

        if direction in "A":  # up arrow pressed
            return "UP"

        if direction in "B":  # down arrow pressed
            return "DOWN"

        # space bar


def less(filename):
    lines = []
    with open(filename) as f:
        lines = f.readlines()

    print(lines)


if __name__ == "__main__":
    print("run tests on less")
