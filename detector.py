import json


def detect(raw_bytes):
    x = {
        "x": 10,
        "y": 30,
        "w": 200,
        "h": 300,
        "class": "test",
    }
    y = {
        "x": 910,
        "y": 230,
        "w": 20,
        "h": 300,
        "class": "test2",
    }
    return json.dumps({
        "type": "boxes",
        "boxes": [x, y],
    })
