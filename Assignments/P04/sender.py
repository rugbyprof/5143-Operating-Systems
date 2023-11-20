from comms import Sender
import sys
import json
from rich import print
from generate_assembly import GenerateAssembly

#Poka, SlipperyDragon149!!!

# rabbitmq_host = "164.90.134.137"  # change as needed
# rabbitmq_user = "user1"  # change to your admin username
# rabbitmq_pass = "123456789"  # change to your admin password
# rabbitmq_port = 5672
# rabbitmq_exch = "cpuproject"

rabbitmq_host = "164.90.134.137"  # change as needed
rabbitmq_user = "Poka"  # change to your admin username
rabbitmq_pass = "SlipperyDragon149!!!"  # change to your admin password
rabbitmq_port = 5672
rabbitmq_exch = "cpuproject"


if __name__ == "__main__":
    with open("commsConfig.json") as f:
        config = json.load(f)

    # if len(sys.argv) < 5:
    #     print("Usage: sender.py <host> <port> <exchange> <routing_key> <message>")
    # else:
    #     print(sys.argv)
    #     host, port, exchange, routing_key, message, num = sys.argv[1:7]

    sender = Sender(**config)
    print(config)
        
    hex = []
    for i in range(10):
        hex.append(GenerateAssembly())
        
    sender.send_message(message=json.dumps(hex),routing_key="hex2",host=rabbitmq_host,port=rabbitmq_port,exchange=rabbitmq_exch)
