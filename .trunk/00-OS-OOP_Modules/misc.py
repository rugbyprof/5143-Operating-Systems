import json

currentId = 4


def isJson(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True


def id():
    global currentId
    temp = currentId
    currentId += 1
    return temp
