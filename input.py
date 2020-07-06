import threading
from pynput.mouse import Button, Controller, Listener as MouseListener
from pynput.keyboard import Key, Listener as KeyListener
from skillautocast import trigger


class InputWorker(threading.Thread):
    def __init__(self, msg_worker):
        threading.Thread.__init__(self)
        self.stopFlag = True
        self.msgWorker = msg_worker
        self.mouse = Controller()

    def stop(self):
        self.stopFlag = True

    def on_release(self, key):
        trigger(key)
        self.msgWorker.send_json({
            "type": "input",
            "source": "keyboard",
            "event": "release",
            "key": '{0}'.format(key)
        })

    def on_move(self, x, y):
        self.msgWorker.send_json({
            "type": "input",
            "source": "mouse",
            "event": "move",
            "x": x,
            "y": y,
        })

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.msgWorker.send_json({
                "type": "input",
                "source": "mouse",
                "event": "click",
                "x": x,
                "y": y,
                "button": '{0}'.format(button),
                "pressed": pressed,
            })

    def run(self):
        self.stopFlag = False
        KeyListener(on_release=self.on_release).start()
        with MouseListener(on_move=self.on_move, on_click=self.on_click) as listener:
            try:
                listener.join()
            except Exception as e:
                print('Done'.format(e.args[0]))
        print('start')
