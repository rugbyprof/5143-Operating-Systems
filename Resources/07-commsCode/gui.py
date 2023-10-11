import PySimpleGUI as sg

import json
from threading import Thread
import sys
import random
from rich import print

from comms import CommsSender, CommsListener


class WindowLocation:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        self.dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        self.usedLocations = []

    def getRandomLoc(self, guiSize=(800, 600)):
        width, height = sg.Window.get_screen_size()
        loc = random.choice(self.dirs)
        while loc in self.usedLocations:
            loc = random.choice(self.dirs)

        self.usedLocations.append(loc)

        if loc == "N":
            return (width // 2, 0)
        elif loc == "NE":
            return (width - guiSize[0], 0)
        elif loc == "E":
            return (width - guiSize[0], height // 2)
        elif loc == "SE":
            return (width - guiSize[0], height - guiSize[1])
        elif loc == "S":
            return (width // 2, height - guiSize[1])
        elif loc == "SW":
            return (0, height - guiSize[1])
        elif loc == "W":
            return (0, height // 2)
        elif loc == "NW":
            return (0, 0)

        return loc


def isJson(jsonData):
    """Checks if a string can be valid json data"""
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True


def main(player, offset):
    W = WindowLocation()

    creds = {
        "exchange": "pygame2d",
        "port": "5672",
        "host": "terrywgriffin.com",
        "user": player,
        "password": "rockpaperscissorsdonkey",
    }

    # create instances of a comms listener and sender
    # to handle message passing.
    commsListener = CommsListener(**creds)
    commsSender = CommsSender(**creds)

    # Start the comms listener to listen for incoming messages
    commsListener.threadedListen()

    theme_names = [
        "black",
        # "DarkBlue14",
        # "DarkGrey12",
        # "DarkGrey13",
        # "DarkGrey14",
        # "DarkGrey15",
        # "DarkPurple6",
        # "DarkPurple7",
    ]

    sg.theme(random.choice(theme_names))

    commands = ("message", "broadcast", "move", "fire")
    targets = ("player-1", "player-2", "player-3", "Everyone")
    layout = [
        [sg.Text("Comms Output....", size=(40, 1))],
        [sg.Output(size=(88, 20), text_color="white", font="Courier 18")],
        [
            sg.Push(),
            sg.Text("Command:", size=(15, 1)),
            sg.Text("Target:", size=(15, 1)),
            sg.Text("Command Body:", size=(15, 1)),
            sg.Text("", size=(25, 1)),
            sg.Push(),
        ],
        [
            sg.Push(),
            sg.Combo(
                commands,
                size=(15, len(commands)),
                key="-COMMAND-",
                enable_events=True,
                default_value="message",
                font="Courier 18",
            ),
            sg.Combo(
                targets,
                size=(15, len(targets)),
                key="-TARGET-",
                enable_events=True,
                default_value="everyone",
                font="Courier 18",
            ),
            sg.Multiline(
                size=(40, 3),
                key="-commandBODY-",
                enable_events=True,
                default_text="",
                font="Courier 18",
                # default_text='{"lat":123.345,"lon":34.234}',
            ),
            sg.Button("Submit", font="Courier 18"),
            sg.Push(),
        ],
    ]

    location = W.getRandomLoc()

    window = sg.Window(f"Comms Panel: {creds['user']}", layout, location=location)

    while True:
        event, values = window.read(timeout=1000)
        if event == "EXIT" or event == sg.WIN_CLOSED:
            break  # exit button clicked
        if event == "Submit":
            # sp = sg.execute_command_subprocess("pip", "list", wait=True)
            command = values["-COMMAND-"]
            target = values["-TARGET-"]
            body = values["-commandBODY-"]
            commsSender.threadedSend(
                target, json.dumps({"command": command, "body": body})
            )

    window.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        player = "player-1"
    else:
        player = sys.argv[1]

    if len(sys.argv) == 3:
        offset = sys.argv[2]
    else:
        offset = None
    main(player, offset)
