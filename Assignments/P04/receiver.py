from comms import Receiver
from comms import mykwargs
import sys
import json


def usage():
    print("Usage: receiver.py <host> <port> <exchange> <routing_keys> ")
    print("Usage: receiver.py 164.90.134.137 5672 cpuproject 'sports,news' ")
    sys.exit()


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

    receiver = Receiver(
        host=host,
        port=port,
        exchange=exchange,
        user=user,
        pword=pword,
        routing_keys="hex2",
    )
    receiver.start_consuming()
