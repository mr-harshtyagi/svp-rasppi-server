from w1thermsensor import W1ThermSensor 
import time
from time import sleep
 
def read_temp():
    try:
        sensor = W1ThermSensor()
        temperature = sensor.get_temperature()
        print(f"Temperature: {temperature}")
    except Exception as e:
        print(f"An error occurred: {e}")
	
while True:
	print(read_temp())	
	time.sleep(1)