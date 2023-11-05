from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
from adxl345 import ADXL345
from w1thermsensor import W1ThermSensor

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
