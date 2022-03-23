import requests

r = requests.get("http://localhost:8080")

print(r.text)
