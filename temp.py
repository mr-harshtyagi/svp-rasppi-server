import Adafruit_DHT

sensor = Adafruit_DHT.DHT11

pin = 21

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        print('Temp={0}*C  Humidity={1}%'.format(temperature, humidity))
        time.sleep(60)
    else:
        print('Failed to get reading. Try again!')
