import threading
import time
from pynput.mouse import Button, Controller


class InputWorker(threading.Thread):
    def __init__(self, msg_worker):
        threading.Thread.__init__(self)
        self.stopFlag = True
        self.msgWorker = msg_worker
        self.mouse = Controller()

    def stop(self):
        self.stopFlag = True

    def run(self):
        self.stopFlag = False
        while not self.stopFlag:
            self.msgWorker.send_json({
                "type": "info",
                "cursor": self.mouse.position,
            })
            time.sleep(0.05)
