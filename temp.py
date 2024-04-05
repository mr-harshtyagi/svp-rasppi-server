#!/usr/bin/python
import sys
import Adafruit_DHT

while True:
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    print(temperature,humidity)