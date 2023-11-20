import pika
import sys
from rich import print
import gzip
import json

with open("commsConfig.json") as f:
    config = json.load(f)


def compress(string_to_compress):
    """Compress a string using gzip compression."""
    compressed_data = gzip.compress(string_to_compress.encode())
    return compressed_data


def decompress(string_to_decompress):
    # Decompress the string
    decompressed_data = gzip.decompress(string_to_decompress)

    # Convert the decompressed data back to a string
    decompressed_string = decompressed_data.decode()

    return decompressed_string


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


class BaseConnection:
    def __init__(self, **kwargs):
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
        credentials = pika.PlainCredentials(self.user, self.pword)
        parameters = pika.ConnectionParameters(self.host, self.port, "/", credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type="topic")


class Receiver(BaseConnection):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # host = kwargs.get("host", config["host"])
        # port = kwargs.get("port", config["port"])
        # exchange = kwargs.get("exchange", config["exchange"])
        # user = kwargs.get("user", config["user"])
        # pword = kwargs.get("pword", config["pword"])
        # routing_keys = kwargs.get("routing_keys", config["routing_keys"])
        # self.binding_keys = binding_keys

    def on_message(self, ch, method, properties, body):
        print(f"Received message: {body.decode()} on topic: {method.routing_key}")

    def start_consuming(self):
        self.connect()
        self.channel.queue_declare(queue="", exclusive=True)
        for key in self.routing_keys:
            self.channel.queue_bind(exchange=self.exchange, queue="", routing_key=key)
        self.channel.basic_consume(
            queue="", on_message_callback=self.on_message, auto_ack=True
        )
        print("Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()


class Sender(BaseConnection):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def send_message(self, **kwargs):
        routing_key = kwargs.get("routing_key", "#")
        message = kwargs.get("message", "Oops")
        self.connect()
        self.channel.basic_publish(
            exchange=self.exchange, routing_key=routing_key, body=message
        )
        print(f"Sent message: {message} on topic: {routing_key}")


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: sender.py <host> <port> <exchange> <routing_key> <message>")
    else:
        host, port, exchange, routing_key, message = sys.argv[1:6]
        sender = Sender(
            host, int(port), exchange, "guest", "guest"
        )  # Assuming default guest credentials
        sender.send_message(routing_key, message)

    # Sending a message to the 'sports' channel
    sender = Sender("localhost", 5672, "my_exchange", "guest", "guest")
    sender.send_message("sports", "Great match today!")

    # Broadcasting a message
    sender.send_message("broadcast", "This is a broadcast message.")

    #### Receiver Code Example

    # Receiver for sports news
    sports_receiver = Receiver(
        "localhost", 5672, "my_exchange", "guest", "guest", ["sports"]
    )
    sports_receiver.start_consuming()

    # Receiver for both sports and news
    news_and_sports_receiver = Receiver(
        "localhost", 5672, "my_exchange", "guest", "guest", ["sports", "news"]
    )
    news_and_sports_receiver.start_consuming()

    # Receiver for all messages
    all_receiver = Receiver("localhost", 5672, "my_exchange", "guest", "guest", ["#"])
    all_receiver.start_consuming()
