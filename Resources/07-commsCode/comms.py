"""
"""
import json
import os
import sys
import time

import pika
import random
from threading import Thread

from rich import print

import gzip


def compress(string_to_compress):
    """Compress a string using gzip compression.
    """
    compressed_data = gzip.compress(string_to_compress.encode())
    return compressed_data



def decompress(string_to_decompress):
    # Decompress the string
    decompressed_data = gzip.decompress(string_to_decompress)

    # Convert the decompressed data back to a string
    decompressed_string = decompressed_data.decode()

    return decompressed_string


class Comms(object):
    """A helper class for client to client messaging. I don't know anything about
    pub/sub so this is rudimentary. In fact, it probably doesn't need to be a
    class! However, I organized it into one simply for encapsulation, keeping
    data and methods together and the added bonus of a constructor etc.
    """

    _messageQueue = {}

    def __init__(self, **kwargs):
        """Remember keyword arguments are params like: key=arg so order doesn't matter.
            The following example shows you how to init an instance of this class.
        Example:
            {
                "exchange": "2dgame",
                "port": "5672",
                "host": "crappy2d.us",
                "user": "yourteamname",
                "password": "yourpassword",
            }
        """
        self.exchange = kwargs.get("exchange", None)
        self.port = kwargs.get("port", 5432)
        self.host = kwargs.get("host", None)
        self.user = kwargs.get("user", None)
        self.password = kwargs.get("password", None)
        self.binding_keys = kwargs.get("binding_keys", [])

        if not self.user in self._messageQueue:
            self._messageQueue[self.user] = []

        self.establishConnection()

    def establishConnection(self, **kwargs):
        """This method basically authenticates with the message server using:

                host, port, user, and password

        After authentication it chooses which "exchange" to listen to. This
        is just like a "channel" in slack. The exchange "type" = "topic" is
        what allows us to use key_bindings to choose which messages to recieve
        based on keywords.
        """
        self.exchange = kwargs.get("exchange", self.exchange)
        self.port = kwargs.get("port", self.port)
        self.host = kwargs.get("host", self.host)
        self.user = kwargs.get("user", self.user)
        self.password = kwargs.get("password", self.password)

        names = ["exchange", "port", "host", "user", "password"]
        params = [self.exchange, self.port, self.host, self.user, self.password]
        for p in zip(names, params):
            if not p[1]:
                print(
                    f"Error: connection parameter `{p[0]}` missing in class Comms method `establishConnection`!"
                )
                sys.exit()

        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(
            self.host, int(self.port), self.exchange, credentials
        )

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type="topic")


class CommsListener(Comms):
    def __init__(self, **kwargs):
        """Extends Comms"""
        self.binding_keys = kwargs.get("binding_keys", [])

        super().__init__(**kwargs)

    def bindKeysToQueue(self, binding_keys=None):
        """https://www.rabbitmq.com/tutorials/tutorial-five-python.html

        A binding key is a way of "subscribing" to a specific messages. Without
        getting to the difference between "routing" and "topics" I will say topics
        should work better for battleship. Valid topics are things like:

           python.javascript.cpp

        This topic would receive any messages from queues containing the routing
        keys: `python` or `javascript` or `cpp`. You can register as many keys as you like.
        But you can also use wild cards:

            * (star) can substitute for exactly one word.
            # (hash) can substitute for zero or more words.

        So if you want to get all messages with your team involved:
            teamname.#
        Or if you want all messages that fire at you:
            teamname.fire.#
        Or if you want to send a message to everyone:
            broadcast.#

        Follow the link above to get a better idea, but at minimum you should
        add binding keys for anything with your teamname (or maybe id) in it.

        """
        result = self.channel.queue_declare("", exclusive=True)
        self.queue_name = result.method.queue

        if binding_keys == None and len(self.binding_keys) == 0:
            self.binding_keys = ["#"]
        elif binding_keys:
            self.binding_keys = binding_keys

        for binding_key in self.binding_keys:
            # print(binding_key)
            self.channel.queue_bind(
                exchange=self.exchange, queue=self.queue_name, routing_key=binding_key
            )

    def startConsuming(self):
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.callback, auto_ack=True
        )
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        """This method gets run when a message is received. You can alter it to
        do whatever is necessary.
        """
        body = decompress(body)
        # self._messageQueue[self.user].append(f"{method.routing_key} : {body}")
        # print(self._messageQueue)
        print(f"{method.routing_key} : {body}")

    def threadedListen(self):
        self.bindKeysToQueue([f"#.{self.user}.#", "#.broadcast.#"])
        Thread(
            target=self.startConsuming,
            args=(),
            daemon=True,
        ).start()


class CommsSender(Comms):
    def __init__(self, **kwargs):
        """Extends Comms and adds a "send" method which sends data to a
        specified channel (exchange).
        """
        super().__init__(**kwargs)

    def send(self, routing_key, body, closeConnection=True):
        if not routing_key:
            print(f"Sending: Broadcasting body: {body}")
        else:
            print(f"Sending: routing_key: {routing_key}, body: {body}")

        body = json.loads(body)

        body["from"] = self.user

        self.channel.basic_publish(
            self.exchange,
            routing_key=f"#.{routing_key}.broadcast",
            body=compress(json.dumps(body)),
        )
        if closeConnection:
            self.connection.close()

    def threadedSend(self, routing_key, body, closeConnection=False):
        print(f"Calling send via Thread")

        Thread(
            target=self.send,
            args=(
                routing_key,
                body,
                closeConnection,
            ),
            daemon=True,
        ).start()

    def closeConnection(self):
        self.connection.close()


def mykwargs(argv):
    """
    Processes argv list into plain args and kwargs.
    Just easier than using a library like argparse for small things.
    Example:
        python file.py arg1 arg2 arg3=val1 arg4=val2 -arg5 -arg6 --arg7
        Would create:
            args[arg1, arg2, -arg5, -arg6, --arg7]
            kargs{arg3 : val1, arg4 : val2}

        Params with dashes (flags) can now be processed seperately
    Shortfalls:
        spaces between k=v would result in bad params
    Returns:
        tuple  (args,kargs)
    """
    args = []
    kargs = {}

    for arg in argv:
        if "=" in arg:
            key, val = arg.split("=")
            kargs[key] = val
        else:
            args.append(arg)
    return args, kargs


def usage(msg):
    print(f"Error: {msg}")
    print("Usage Syntax:")
    print("    square brackets imply: \[optional param]")
    print("    angle brackets imply: <required>")
    print("    curly braces show: {default value}")
    print(
        """
    Usage: python CommsClass direction=<send,listen>  
                             player=<playerId> 
                             game=<gameId> 
                             target=<playerId> 
                             message=['your message']{default='This is a message.'} 
                             rounds=[n]{default = 3,-1 = continue sending until ctrl-c to quit}
                             
        direction : sender and listener
        player : sender and listener
        game : sender and listener
        target : sender only
        message : sender only
        round : sender only
        """
    )
    print("Examples: ")
    name  = os.path.basename(__file__)
    print(
        f"""
    Basic Listener:
        python {name} direction=listener player=player-07 game=game-03
        (starts a lister listening on queue: game-03 and using playerId : player07)
    Basic Sender: 
        python {name} direction=sender player=player-05 game=game-03 target=player-07)
        (starts a sender who sends a message to `player-07 using the queue `game-03` sending as `player04` the message: `This is a message.` 3 times.)
        
        python {name} direction=sender player=player-04 game=game-03 target=player-21 message='{{x:80,y:200,velocity:3}}' rounds=50)
        (starts a sender who sends a message to `player-21 using the queue `game-03` sending as `player04` the message: `{{x:80,y:200,velocity:3}}` 50 times.)
        
        python {name} direction=sender player=player-04 game=game-03 target=player-21 message='{{x:80,y:200,velocity:3}}' rounds=-1)
        (starts a sender who sends a message to `player-21 using the queue `game-03` sending as `player04` the message: `{{x:80,y:200,velocity:3}}` until ctrl-c is hit.)
        """
    )
    sys.exit()


if __name__ == "__main__":
    args, kwargs = mykwargs(sys.argv)

    direction = kwargs.get("direction", None)
    player = kwargs.get("player", None)
    game = kwargs.get("game", None)
    target = kwargs.get("target", None)
    message = kwargs.get("message", "This is a message.")
    rounds = int(kwargs.get("rounds", 3))
    sleepTime = float(kwargs.get("sleepTime", 0.5))

    if int(rounds) < 0:
        rounds = pow(2, 20)

    if direction == None:
        usage("`direction` needed in command params.")
    elif direction == "sender":
        #if None in [game, player, target]:
        if None in [game, player]:
            usage(
                "`game`, `target` and `player` needed in command params to send a message."
            )
    elif direction == "listen":
        if None in [game, player]:
            usage(
                "`game` and `player` needed in command params to listen for messages."
            )

    queues = []
    for i in range(10):
        i += 1
        if i < 10:
            q = "0" + str(i)
        queues.append("game-" + q)
    users = []
    for i in range(25):
        if i < 10:
            p = "0" + str(i)
        queues.append("player-" + p)

    creds = {
        "exchange": game,
        "port": "5672",
        "host": "terrywgriffin.com",
        "user": player,
        "password": player + "2023!!!!!",  # user.capitalize() * 3,
    }

    if direction == "sender":
        commsSender = CommsSender(**creds)
        for i in range(rounds):
            commsSender.send(target, json.dumps({"data": message}), False)
            time.sleep(sleepTime)
            print(f"sending message: {i}")
            print(f"sleeping for {sleepTime} seconds")

    else:
        print(
            f"Comms Listener starting for {player} on {game}. To exit press CTRL+C ..."
        )
        commsListener = CommsListener(**creds)
        commsListener.bindKeysToQueue([f"#.{game}.#", "#.broadcast.#"])
        commsListener.startConsuming()
