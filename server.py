import asyncio
import websockets
import time
import json
import random
from flask import Flask, request
app = Flask(__name__)

# a websocket client
async def sensor_data_sender():
    uri = "ws://localhost:4000"  # replace with your Node.js server URI
    try:
        async with websockets.connect(uri) as websocket:
            n = 5
            while True:
                # Simulate sensor data
                sensor_data = {"temperature": random.uniform(20.0, 60.0), "acc": random.uniform(0.0, 8.0), "time": time.time()}
                print("Sending data:", sensor_data)
                await websocket.send(json.dumps(sensor_data))
                await asyncio.sleep(1)  # sleep for 1 second
                n -= 1
    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed. Server is Offline. Retrying...")
        await asyncio.sleep(5)  # sleep for 5 seconds before retrying
        await sensor_data_sender()  # recursively call the function to retry the connection
    except Exception as e:
        print("An error occurred:", str(e))

asyncio.get_event_loop().run_until_complete(sensor_data_sender())
