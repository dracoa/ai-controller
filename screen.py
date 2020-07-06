#!/usr/bin/env python3
import threading
import mss
import mss.tools
from skillautocast import update_screen
import time
from PIL import Image
import io


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
                sct_img = sct.grab(monitor)
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                imgBytes = io.BytesIO()
                img.save(imgBytes, format="JPEG")
                self.msgWorker.send_binary(imgBytes.getvalue())
                result = update_screen(img)
                self.msgWorker.send_json({
                    "type": "info",
                    "autoCast": result
                })
                time.sleep(1 / 30)
