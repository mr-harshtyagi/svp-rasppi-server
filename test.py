# Running on Raspberry Pi 4B
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
# import asyncio
import websockets
import json
import socketio
import schedule
import time
import random

from adxl345 import ADXL345
from w1thermsensor import W1ThermSensor
import RPi.GPIO as GPIO

sio = socketio.Client()

app = Flask(__name__)
socketio = SocketIO(app)

# Set the PWM pin number and frequency
pwm_pin1 = 18
# pwm_pin2 = 19

# Initialize the PWM Pin 1
GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm_pin1, GPIO.OUT)
pwmPin1 = GPIO.PWM(pwm_pin1, 100)


mrValue = 0
smaValue = 0
motorSpeed = 0
interval = 0.1

# reading data from sensors
temperature = 25
acceleration = 0

pwmPin1.start(0)  # 0% duty cycle

# set pwn duty cycle functions
def set_pwm1(duty_cycle):
    pwmPin1.ChangeDutyCycle(duty_cycle)

# Stop PWM
pwmPin1.stop()

# Clean up GPIO
GPIO.cleanup()

# Initialize the PWM Pin 2
# GPIO.setup(pwm_pin2, GPIO.OUT, initial=GPIO.LOW)
# pwmPin2 = GPIO.PWM(pwm_pin2, 100)
# pwmPin2.start(0)

# def set_pwm2(duty_cycle):
#     pwmPin2.ChangeDutyCycle(duty_cycle)


# get sensor data functions

# def get_temperature_data():
#     sensor = W1ThermSensor()
#     temperature = sensor.get_temperature()
#     return jsonify({'temperature': temperature})

def get_accelerometer_data():
    accelerometer = ADXL345()
    data = accelerometer.get_axes(True)
    return ( data['y'])

# @app.route('/')
# def index():
#     return render_template('index.html')



# SocketIO Client
# This job function sends data to the server every "interval" seconds
def job():
    global temperature, acceleration
    # temperature = get_temperature_data()
    acceleration = get_accelerometer_data()
    # print('Temperature:', temperature, 'Acceleration:', acceleration)
    # get acc and temo data points from sensors and set data here : TO DO
    # data = {
    #     'smaValue':smaValue,
    #     'mrValue':mrValue,
    #     'motorSpeed':motorSpeed,
    #     'temp': round(40 + random.random()*40, 2),
    #     'acc': round(random.random()*10, 2),
    #     'time': time.time()
    #     }
    data = {
        'smaValue':smaValue,
        'mrValue':mrValue,
        'motorSpeed':motorSpeed,
        'temp': temperature,
        'acc': acceleration,
        # 'time': time.time()
        }
    # print("Sendind data to server : ",data)

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
    print("Motor Speed : ", motorSpeed) 
    set_pwm1(motorSpeed)

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

sio.connect('https://api.smsl.online', auth={'token': 'rasppi-server-token','type':'experiment'})
# sio.connect('http://localhost:4000', auth={'token': 'rasppi-server-token','type':'experiment'})

if __name__ == '__main__':
    socketio.run(app) 