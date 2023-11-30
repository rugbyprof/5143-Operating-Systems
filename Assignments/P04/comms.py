import pika
import sys
from rich import print

import json

class Comms:
    """Base class for a RabbitMQ connection.
    """
    def __init__(self, **kwargs):
        """Constructor for BaseConnection class.
        Params:
            host (str): IP address of the RabbitMQ server
            port (int): Port number of the RabbitMQ server
            exchange (str): Name of the exchange to connect to
            user (str): Username for the RabbitMQ server
            pword (str): Password for the RabbitMQ server
            routing_keys (list<str>): List of routing keys to bind to
        """
        config = kwargs.get("config", None)
        if config:
            with open(config) as f:
                config = json.load(f)
            for k,v in config.items():
                self.__dict__[k] = v
        else:
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
    def __str__(self):
        return (f"Comms(host={self.host}, port={self.port}, exchange={self.exchange}, "
                f"user={self.user}, routing_keys={self.routing_keys})")
    def __repr__(self):
        return (f"Comms(host={repr(self.host)}, port={repr(self.port)}, "
                f"exchange={repr(self.exchange)}, user={repr(self.user)}, "
                f"pword='******', routing_keys={repr(self.routing_keys)})")
    def connect(self):
        """_summary_"""
        credentials = pika.PlainCredentials(self.user, self.pword)
        parameters = pika.ConnectionParameters(self.host, self.port, "/", credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type="topic")

class Receiver(Comms):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(kwargs)
        if 'callback' in kwargs:
            self.callback = kwargs['callback']  # callback function to call when a message is received
        else:
            self.callback = self.on_message
        print(f"self.callback: {self.callback}")
        print(f"self.on.message: {self.on_message}")

        # host = kwargs.get("host", config["host"])se
        # port = kwargs.get("port", config["port"])
        # exchange = kwargs.get("exchange", config["exchange"])
        # user = kwargs.get("user", config["user"])
        # pword = kwargs.get("pword", config["pword"])
        # routing_keys = kwargs.get("routing_keys", config["routing_keys"])
        # self.binding_keys = binding_keys

    def on_message(self, ch, method, properties, body):
        print(f"Received message: {body.decode()} on topic: {method.routing_key}")
    
# # Declare queues for each group
# channel.queue_declare(queue='group1_queue')

    def start_consuming(self):
        self.connect()
        self.channel.queue_declare(queue="scales_queue")
        # for key in self.routing_keys:
        #     self.channel.queue_bind(exchange=self.exchange, queue="", routing_key=key)
        self.channel.queue_bind(exchange=self.exchange, queue="scales_queue", routing_key='scales.#')
        self.channel.basic_consume(
            queue="scales_queue", on_message_callback=self.callback, auto_ack=True
        )

        print("Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()


class Sender(Comms):
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