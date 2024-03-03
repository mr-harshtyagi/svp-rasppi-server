# Running on Raspberry Pi 4B
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
# import asyncio
import websockets
# import json
import socketio
import schedule
import time
import random

# from adxl345 import ADXL345
# from w1thermsensor import W1ThermSensor
# import RPi.GPIO as GPIO

sio = socketio.Client()

app = Flask(__name__)
socketio = SocketIO(app)

# # Set the PWM pin number and frequency
# pwm_pin1 = 18
# pwm_pin2 = 19

# # Initialize the PWM Pin 1
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(pwm_pin1, GPIO.OUT, initial=GPIO.LOW)
# pwmPin1 = GPIO.PWM(pwm_pin1, 100)
# pwmPin1.start(0)

# # Initialize the PWM Pin 2
# GPIO.setup(pwm_pin2, GPIO.OUT, initial=GPIO.LOW)
# pwmPin2 = GPIO.PWM(pwm_pin2, 100)
# pwmPin2.start(0)

# # set pwn duty cycle functions
# def set_pwm1(duty_cycle):
#     pwmPin1.ChangeDutyCycle(duty_cycle)

# def set_pwm2(duty_cycle):
#     pwmPin2.ChangeDutyCycle(duty_cycle)


# get sensor data functions

def get_temperature_data():
    sensor = W1ThermSensor()
    temperature = sensor.get_temperature()
    return jsonify({'temperature': temperature})

def get_accelerometer_data():
    accelerometer = ADXL345()
    data = accelerometer.get_axes(True)
    return jsonify(data)

# @app.route('/')
# def index():
#     return render_template('index.html')

mrValue = 0
smaValue = 0
motorSpeed = 0
interval = 0.1

# SocketIO Client
# This job function sends data to the server every "interval" seconds
def job():
    # get acc and temo data points from sensors and set data here : TO DO
    data = {
        'smaValue':smaValue,
        'mrValue':mrValue,
        'motorSpeed':motorSpeed,
        'temp': round(40 + random.random()*40, 2),
        'acc': round(random.random()*10, 2),
        'time': time.time()
        }
    print("Sendind data to server : ",data)
    sio.emit('svpRaspPiMessage', data)  

def on_server_response(data):
    global mrValue, smaValue, motorSpeed
    print('I received a response from server!')

    # If you want to access the data sent with the event:
    print('Response : ', data)
    mrValue = data['mrValue']
    smaValue = data['smaValue']
    motorSpeed = data['motorSpeed']

    # Trigger MR, SMA and motors based on above values received: TO DO

@sio.event
def connect():
    schedule.every(interval).seconds.do(job)
    while True:
        schedule.run_pending()

sio.on('svpServerResponse', on_server_response)

# try:
#     sio.connect('https://api.smsl.online')
# except socketio.exceptions.ConnectionError as e:
#     print(f"Failed to connect to server: {e}")

sio.connect('https://api.smsl.online')

if __name__ == '__main__':
    socketio.run(app) 