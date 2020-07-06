from pynput.mouse import Button, Controller, Listener as MouseListener
from pynput.keyboard import Key, Controller
import time
import numpy as np
import matplotlib.pyplot as plt

keyboard = Controller()

skills = [
    {
        "trigger": "Key.f6",
        "action": "1",
        "condition": "4s",  # interval 4 seconds
        "box": {"x": 626, "y": 989, "w": 64, "h": 72},
        "state": "off",
        "text": "1",
    },
    {
        "trigger": "Key.f7",
        "action": "2",
        "condition": "none_effect",
        "box": {"x": 693, "y": 989, "w": 64, "h": 72},
        "state": "off",
        "text": "1",
    },
    {
        "trigger": "Key.f8",
        "action": "3",
        "condition": "none_effect",
        "box": {"x": 759, "y": 989, "w": 64, "h": 72},
        "state": "off",
        "text": "1",
    },
    {
        "trigger": "Key.f9",
        "action": "4",
        "condition": "none_effect",
        "box": {"x": 827, "y": 989, "w": 64, "h": 72},
        "state": "off",
        "text": "1",
    },
    {
        "trigger": "Key.f10",
        "action": "Button.left",
        "condition": "available",
        "box": {"x": 895, "y": 989, "w": 64, "h": 72},
        "state": "off",
        "text": "1",
    },
    {
        "trigger": "Key.f11",
        "action": "6",
        "condition": "None",  # one press on_off
        "box": {"x": 962, "y": 989, "w": 64, "h": 72},
        "state": "off",
        "text": "1",
    }
]
skill_map = {}
for s in skills:
    s["last"] = time.time()
    skill_map[s["trigger"]] = s

print(skill_map)


def trigger(key):
    ts = skill_map.get('{0}'.format(key), None)
    if ts is not None:
        if ts["state"] == "on":
            ts["state"] = "off"
            ts["text"] = "off"
        elif ts["state"] == "off":
            ts["state"] = "on"
            ts["text"] = "on"
            ts["last"] = time.time()


def update_screen(img):
    for value in skill_map.values():
        process(img, value)
    return {
        "type": "auto-cast",
        "skills": skill_map,
    }


def process(img, skill):
    cond = skill.get("condition", None)

    if skill.get("state", "off") == "on":
        if cond.endswith("s"):
            interval(img, skill)
        elif cond == "available":
            available(img, skill)
        elif cond == "none_effect":
            none_effect(img, skill)


def interval(img, skill):
    cond = skill.get("condition", None)
    diff = time.time() - skill.get("last", 0)
    secs = float(cond[:-1])
    if diff > secs:
        keyboard.press(skill.get("action"))
        keyboard.release(skill.get("action"))
        skill["last"] = time.time()


def available(img, skill):
    print("not yet implement")


def none_effect(img, skill):
    if effect_histrogrtam(img, skill):
        keyboard.press(skill.get("action"))
        keyboard.release(skill.get("action"))
        skill["last"] = time.time()


def effect_histrogrtam(img, skill):
    box = skill["box"]
    left = box["x"] + 10
    top = box["y"] + 6
    right = left + 46
    bottom = top + 3
    crop = img.crop((left, top, right, bottom))
    red, green, blue = crop.split()
    histogram, bin_edges = np.histogram(green, bins=8, range=(0, 255))
    return (histogram[0] + histogram[1]) > 130
