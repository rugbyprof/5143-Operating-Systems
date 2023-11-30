from comms import Receiver
from toolbox import mykwargs
import sys
import json


def usage():
    print("Usage: receiver.py <host> <port> <exchange> <routing_keys> ")
    print("Usage: receiver.py 164.90.134.137 5672 cpuproject 'sports,news' ")
    sys.exit()


def processMessage(ch, method, properties, body):
    print(f"I will not beat off any more")
    data = json.loads(body.decode())
    for instructions in data:
        for i in instructions:
            print(i)

        # print(instructions)


class Decoder:
    def __init__(self, config="commsConfig.json", callback=processMessage):
        print(processMessage)
        self.receiver = Receiver(config=config, callback=processMessage)
        self.receiver.start_consuming()


if __name__ == "__main__":
    with open("commsConfig.json") as f:
        config = json.load(f)

    print(config)

    args, kwargs = mykwargs(sys.argv)
    keys = list(kwargs.keys())
    if "help" in kwargs:
        usage()

    else:
        host = kwargs.get("host", config["host"])
        port = kwargs.get("port", config["port"])
        exchange = kwargs.get("exchange", config["exchange"])
        user = kwargs.get("user", config["user"])
        pword = kwargs.get("pword", config["pword"])
        routing_keys = kwargs.get("routing_keys", config["routing_keys"])
        if not isinstance(routing_keys, list):
            routing_keys = routing_keys.split(",")

        #### Receiver Code Example

    # receiver = Receiver(
    #     host=host,
    #     port=port,
    #     exchange=exchange,
    #     user=user,
    #     pword=pword,
    #     routing_keys="hex2",
    # )
    # receiver=Receiver(config="commsConfig.json")
    # receiver.start_consuming()
    decoder = Decoder(config="commsConfig.json", callback=processMessage)
