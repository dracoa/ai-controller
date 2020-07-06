from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
box = {"x": 693, "y": 989, "w": 64, "h": 72}


img = Image.open(r"b.png")
width, height = img.size
print(img.size)
left = box["x"] + 8
top = box["y"] + 15
right = left + 48
bottom = top + 48
print(left, top, right, bottom)
crop = img.crop((left, top, right, bottom))
plt.imshow(crop)
plt.show()
