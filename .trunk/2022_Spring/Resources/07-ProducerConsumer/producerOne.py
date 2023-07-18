import requests
from rich import print
from random import choice
from random import randint

valid_instructions = ["ADD", "SUB", "MUL", "SET"]
locations = [chr(x + 65) for x in range(26)]

payloads = []

for i in range(5):
    payloads.append(
        {
            "op": choice(valid_instructions),
            "val": randint(1, 100),
            "loc": choice(locations),
        }
    )

url = "http://127.0.0.1:8080/produceOne/"

# print(payloads[0].values())

r = requests.post(url, json=payloads[0])

print(r.json())
