

def detect(raw_bytes):
    x = {
        "x": 0,
        "y": 0,
        "w": 10,
        "h": 10,
        "class": "1",
    }
    y = {
        "x": 1910,
        "y": 1070,
        "w": 10,
        "h": 10,
        "class": "2",
    }
    return {
        "type": "boxes",
        "boxes": [x, y],
    }
