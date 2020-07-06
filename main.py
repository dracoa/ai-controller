#!/usr/bin/env python3
import sys
import websockets
import asyncio
import json
from screen import MssWorker
from input import InputWorker

sys.path.append('.')
stopFlag = False


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

    def send_data(self, data):
        for websocket in self.connected.copy():
            coro = websocket.send(data)
            _ = asyncio.run_coroutine_threadsafe(coro, loop)

    def send_binary(self, data):
        self.send_data(data)

    def send_json(self, data):
        self.send_data(json.dumps(data))


if __name__ == "__main__":
    print('ai-controller server')
    msgWorker = WsWorker()
    mssWorker = MssWorker(msgWorker)
    inputWorker = InputWorker(msgWorker)
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
