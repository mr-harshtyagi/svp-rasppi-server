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
import threading

from adxl345 import ADXL345
from w1thermsensor import W1ThermSensor
import RPi.GPIO as GPIO

sio = socketio.Client()

app = Flask(__name__)
socketio = SocketIO(app)

# Set the PWM pin number and frequency
pwm_pin1 = 32
pwm_pin2 = 33
pwm_pin3 = 12
# pwm_pin2 = 19

# Initialize the PWM Pin 1
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pwm_pin1, GPIO.OUT)

pwmPin1 = GPIO.PWM(pwm_pin1, 100)
pwmPin1.start(0)  # 0% duty cycle

# Initialize the PWM Pin 2
GPIO.setup(pwm_pin2, GPIO.OUT, initial=GPIO.LOW)
pwmPin2 = GPIO.PWM(pwm_pin2, 100)
pwmPin2.start(0)

# Initialize the PWM Pin 3
GPIO.setup(pwm_pin3, GPIO.OUT, initial=GPIO.LOW)
pwmPin3 = GPIO.PWM(pwm_pin3, 100)
pwmPin3.start(0)

mrValue = 0
smaValue = 0
motorSpeed = 0
interval = 0.1
previousMotorSpeed = 0

# reading data from sensors
temperature = 25
acceleration = 0

# set pwn duty cycle functions
def set_pwm1(duty_cycle):
    pwmPin1.ChangeDutyCycle(duty_cycle)

def set_pwm2(duty_cycle):
    pwmPin2.ChangeDutyCycle(duty_cycle)

def set_pwm3(duty_cycle):
    pwmPin3.ChangeDutyCycle(duty_cycle)

def get_temperature_data():
    global temperature
    try:
        sensor = W1ThermSensor()
        temperature = sensor.get_temperature()
        print(f"Temperature: {temperature}")
        return temperature
    except Exception as e:
        print(f"An error occurred: {e}")
        return temperature

def get_accelerometer_data():
    global acceleration
    try:
        accelerometer = ADXL345()
        data = accelerometer.get_axes()
        # print(data)
        return data['y']
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return acceleration

# SocketIO Client
# This job function sends data to the server every "interval" seconds
def job():
    global temperature, acceleration , mrValue, smaValue, motorSpeed, previousMotorSpeed
    # temperature = get_temperature_data()
    while True:
        acceleration = get_accelerometer_data()
        temperature = get_temperature_data()
        data = {
            'smaValue':smaValue,
            'mrValue':mrValue,
            'motorSpeed':motorSpeed,
            'temp': temperature,
            'acc': acceleration,
            }
        sio.emit('svpRaspPiMessage', data)
        time.sleep(interval)

def start_job_in_new_thread():
    print('Starting job in new thread')
    thread = threading.Thread(target=job)
    thread.start()

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
    print("SMA Value : ", smaValue)
    set_pwm2(smaValue)
    print("MR Value : ", mrValue)
    set_pwm3(mrValue)

@sio.event
def connect():
    print('connection established, start job')
    start_job_in_new_thread()

sio.on('svpServerResponse', on_server_response)

sio.connect('https://api.smsl.online', auth={'token': 'rasppi-server-token','type':'experiment'})
# sio.connect('http://localhost:4000', auth={'token': 'rasppi-server-token','type':'experiment'})

if __name__ == '__main__':
    socketio.run(app) 

