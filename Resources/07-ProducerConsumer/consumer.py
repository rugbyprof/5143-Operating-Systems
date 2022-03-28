import requests
from rich import print

r = requests.get("http://localhost:8080/consume")

print(r.json())
