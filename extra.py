#!/usr/bin/env python3
import threading
import mss
import mss.tools
from detector import detect

class MssWorker(threading.Thread):
    def __init__(self, msg_worker):
        threading.Thread.__init__(self)
        self.stopFlag = True
        self.msgWorker = msg_worker

    def stop(self):
        self.stopFlag = True

    def run(self):
        self.stopFlag = False
        with mss.mss() as sct:
            monitor_number = 1  # TODO - change monitor on the fly
            mon = sct.monitors[monitor_number]
            print(mon)
            monitor = {
                "top": mon["top"],  # 100px from the top
                "left": mon["left"],  # 100px from the left
                "width": mon["width"],
                "height": mon["height"],
                "mon": monitor_number,
            }
            while not self.stopFlag:
                im = sct.grab(monitor)
                raw_bytes = mss.tools.to_png(im.rgb, im.size)
                self.msgWorker.sendData(raw_bytes)
                boxes = detect(raw_bytes)
                self.msgWorker.sendData(boxes)
