#!/usr/bin/env python3
import sys
import time
import websockets
import asyncio
import threading
from extra import MssWorker

sys.path.append('.')
stopFlag = False


class InputWorker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while not stopFlag:
            time.sleep(1)


class WsWorker:
    def __init__(self):
        self.connected = set()

    async def handler(self, websocket, path):
        self.connected.add(websocket)
        print("connection starts")
        try:
            while not stopFlag:
                msg = await websocket.recv()
                print(msg)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.connected.remove(websocket)

    def sendData(self, data):
        for websocket in self.connected.copy():
            coro = websocket.send(data)
            _ = asyncio.run_coroutine_threadsafe(coro, loop)


if __name__ == "__main__":
    print('ai-controller server')
    msgWorker = WsWorker()
    mssWorker = MssWorker(msgWorker)
    inputWorker = InputWorker()
    try:
        mssWorker.start()
        inputWorker.start()
        ws_server = websockets.serve(msgWorker.handler, '0.0.0.0', 7700)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(ws_server)
        loop.run_forever()
    except KeyboardInterrupt:
        stopFlag = True
        # TODO: close ws server and loop correctely
        print("Exiting program...")
