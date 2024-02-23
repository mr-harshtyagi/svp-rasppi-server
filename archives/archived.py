from flask import Flask, jsonify, render_template,request
from flask_socketio import SocketIO, emit
from adxl345 import ADXL345
from w1thermsensor import W1ThermSensor
import RPi.GPIO as GPIO

app = Flask(__name__)

# Set the PWM pin number and frequency
pwm_pin1 = 18
pwm_pin2 = 19

# Initialize the PWM Pin 1
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pwm_pin1, GPIO.OUT, initial=GPIO.LOW)
pwmPin1 = GPIO.PWM(pwm_pin1, 100)
pwmPin1.start(0)

# Initialize the PWM Pin 2
GPIO.setup(pwm_pin2, GPIO.OUT, initial=GPIO.LOW)
pwmPin2 = GPIO.PWM(pwm_pin2, 100)
pwmPin2.start(0)

socketio = SocketIO(app,cors_allowed_origins="*")  # Enable cross-origin access

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_pwm1', methods=['POST'])
def set_pwm1():
    print(request.form)
    duty_cycle = int(request.form['duty_cycle'])
    pwmPin1.ChangeDutyCycle(duty_cycle)
    return render_template('index.html')

@app.route('/set_pwm2', methods=['POST'])
def set_pwm2():
    duty_cycle = int(request.form['duty_cycle'])
    pwmPin2.ChangeDutyCycle(duty_cycle)
    return 'PWM duty cycle set to {}'.format(duty_cycle)

@app.route('/accelerometer')
def get_accelerometer_data():
    accelerometer = ADXL345()
    data = accelerometer.get_axes(True)
    return jsonify(data)

@app.route('/temperature')
def get_temperature_data():
    sensor = W1ThermSensor()
    temperature = sensor.get_temperature()
    return jsonify({'temperature': temperature})

@app.route('/accelerometer_stream')
def stream_accelerometer_data():
    accelerometer = ADXL345()
    while True:
        data = accelerometer.get_axes(True)
        emit('accelerometer_data', data)
        socketio.sleep(1)  # Update every 1 second

@app.route('/temperature_stream')
def stream_temperature_data():
    sensor = W1ThermSensor()
    while True:
        temperature = sensor.get_temperature()
        emit('temperature_data', {'temperature': temperature})
        socketio.sleep(1)  # Update every 1 second


# Inside your Flask routes, where you want to send data
@app.route('/send_data_to_central_server')
def send_data_to_central_server():
    # Collect your sensor data (replace with your actual data collection logic)
    accelerometer_data = {'x': 0.12, 'y': -0.34, 'z': 9.81}
    temperature_data = {'temperature': 23.5}

    # Send data to the central server
    socketio.emit('sensor_data', {'accelerometer': accelerometer_data, 'temperature': temperature_data}, namespace='/central')
    return 'Data sent to central server'

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
