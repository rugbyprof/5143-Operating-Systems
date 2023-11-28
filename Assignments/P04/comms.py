import pika
import sys
from rich import print
import gzip
import json

with open("commsConfig.json") as f:
    config = json.load(f)


def compress(string_to_compress):
    """ Compress a string using gzip compression.
    Params: string_to_compress (str)
    Returns: compressed_data (bytes)
    """
    compressed_data = gzip.compress(string_to_compress.encode())
    return compressed_data


def decompress(string_to_decompress):
    """ Decompress a string using gzip compression.
    Params: string_to_decompress (bytes)
    Returns: decompressed_string (str)
    """
    # Decompress the string
    decompressed_data = gzip.decompress(string_to_decompress)

    # Convert the decompressed data back to a string
    decompressed_string = decompressed_data.decode()

    return decompressed_string


def mykwargs(argv):
    """ Processes argv list into plain args and kwargs.
        Just easier than using a library like argparse for small things.
    Params:
        argv (list<str>): list of command line arguments to process
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


class BaseConnection:
    """ Base class for a RabbitMQ connection.
        host=host, port=int(port), exchange=exch, user=user, pword=pword, routing_keys=keys
    """
    def __init__(self, **kwargs):
        """ Constructor for BaseConnection class.
        Params:
            host (str): IP address of the RabbitMQ server
            port (int): Port number of the RabbitMQ server
            exchange (str): Name of the exchange to connect to
            user (str): Username for the RabbitMQ server
            pword (str): Password for the RabbitMQ server
            routing_keys (list<str>): List of routing keys to bind to
        """
        self.host = kwargs.get("host", config["host"])
        self.port = kwargs.get("port", config["port"])
        self.exchange = kwargs.get("exchange", config["exchange"])
        self.user = kwargs.get("user", config["user"])
        self.pword = kwargs.get("pword", config["pword"])
        self.routing_keys = kwargs.get("routing_keys", config["routing_keys"])
        
        if not isinstance(self.routing_keys, list):
            self.routing_keys = self.routing_keys.split(",")

        self.connection = None
        self.channel = None

        if not self.user or not self.pword:
            print("Error: need to instantiate class with a user and password!")
            sys.exit()

    def connect(self):
        """_summary_
        """
        credentials = pika.PlainCredentials(self.user, self.pword)
        parameters = pika.ConnectionParameters(self.host, self.port, "/", credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type="topic")


class Receiver(BaseConnection):
    """_summary_

    Args:
        BaseConnection (_type_): _description_
    """
    def __init__(self, **kwargs):
        """
        Params:
            host (str): IP address of the RabbitMQ server
            port (int): Port number of the RabbitMQ server
            exchange (str): Name of the exchange to connect to
            user (str): Username for the RabbitMQ server
            pword (str): Password for the RabbitMQ server
            routing_keys (list<str>): List of routing keys to bind to
        """
        super().__init__(**kwargs)
        
        if 'callback' in kwargs:
            self.callback = kwargs['callback']  # callback function to call when a message is received
        else:
            self.callback = self.on_message

    def on_message(self, ch, method, properties, body):
        print(f"Received message: {body.decode()} on topic: {method.routing_key}")

    def start_consuming(self):
        self.connect()
        self.channel.queue_declare(queue="", exclusive=True)
        for key in self.routing_keys:
            self.channel.queue_bind(exchange=self.exchange, queue="", routing_key=key)
        self.channel.basic_consume(
            queue="", on_message_callback=self.callback, auto_ack=True
        )
        print("Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()


class Sender(BaseConnection):
    def __init__(self, **kwargs):
        """
        host=host, port=int(port), exchange=exch, user=user, pword=pword, routing_keys=keys
        """
        super().__init__(**kwargs)
        

    def send_message(self, **kwargs):
        routing_keys = kwargs.get("routing_keys", "#")
        message = kwargs.get("message", "Oops")
        self.connect()
        self.channel.basic_publish(
            exchange=self.exchange, routing_keys=routing_keys, body=message
        )
        print(f"Sent message: {message} on topic: {routing_keys}")


if __name__ == "__main__":
    """
    host=host, port=int(port), exchange=exch, user=user, pword=pword, routing_keys=keys
    """
    if len(sys.argv) < 6:
        print("Usage: comms.py <host> <port> <sender/receiver> <user> <pass> <exchange> <routing_key> <message>")
        host = "164.90.134.137"  # change as needed
        port = 5672
        sendrec = "sender"
        user = "Poka"  # change to your admin username
        pword = "SlipperyDragon149!!!"  # change to your admin password
        exch = "cpuproject"
        keys = "data"
        message = "{address: 0x0000, value: 0x0000, type: 'read'}"
        print(f"Example values: host={host} port={port} sendrec={sendrec} user={user} pword={pword} exchange={exch} keys={keys} message={message}")
        sys.exit()
    else:
        host, port, sendrec, user, pword, exch, keys, message = sys.argv[1:7]
        keys = keys.split(",")
        if sendrec == "sender":
            sender = Sender(
                host=host, port=int(port), exchange=exch, user=user, pword=pword,keys=keys
            ) 
            sender.send_message(keys, message)
        else: # receiver
            receiver = Receiver(
                host=host, port=int(port), exchange=exch, user=user, pword=pword, keys=keys
            )
            receiver.start_consuming()

    # Sending a message to the 'sports' channel
    # sender = Sender(host, port, exch, user, pwrd)
    # sender.send_message("sports", "Great match today!")

    # # Broadcasting a message
    # sender.send_message("broadcast", "This is a broadcast message.")

    # #### Receiver Code Example

    # # Receiver for sports news
    # sports_receiver = Receiver(
    #     "localhost", 5672, "my_exchange", "guest", "guest", ["sports"]
    # )
    # sports_receiver.start_consuming()

    # # Receiver for both sports and news
    # news_and_sports_receiver = Receiver(
    #     "localhost", 5672, "my_exchange", "guest", "guest", ["sports", "news"]
    # )
    # news_and_sports_receiver.start_consuming()

    # # Receiver for all messages
    # all_receiver = Receiver("localhost", 5672, "my_exchange", "guest", "guest", ["#"])
    # all_receiver.start_consuming()


