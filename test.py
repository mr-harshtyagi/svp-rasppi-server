# Running on Raspberry Pi 4B
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import asyncio
import websockets
import json
import socketio
import schedule
import time
import random

sio = socketio.Client()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

# SocketIO Client

def job():
    print("I'm connected to server!")
    sio.emit('test', {'data': random.random(), 'time': time.time()})  

@sio.event
def connect():
    schedule.every(0.01).seconds.do(job)

    while True:
        schedule.run_pending()

@sio.on('testResponse')
def on_test(data):
    print('I received a response from server!')

    # If you want to access the data sent with the event:
    print('Reponse : ', data)

# Backend Server
sio.connect('http://localhost:4000')

if __name__ == '__main__':
    socketio.run(app)