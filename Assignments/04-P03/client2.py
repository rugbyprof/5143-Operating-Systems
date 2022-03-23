import requests

pload = {"data": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}

r = requests.post("http://localhost:8080", data=pload)

print(r.json())
