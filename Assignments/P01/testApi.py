import requests
import json


def test_api():
    # Make a GET request to the API
    response = requests.get("http://127.0.0.1:8080/files/")

    print(response.status_code)

    if response.status_code == 200:
        print("API is working!")
    jdata = response.json()

    print(jdata)


test_api()
