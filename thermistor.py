from machine import ADC
from time import sleep
import math

adcpin = 26
thermistor = ADC(adcpin)

# Voltage Divider
Vin = 3.3
Ro = 10000  # 10k Resistor

# Steinhart Constants
A = 0.001129148
B = 0.000234125
C = 0.0000000876741

while True:
    # Get Voltage value from ADC   
    adc = thermistor.read_u16()
    Vout = (3.3/65535)*adc
    
    # Calculate Resistance
    Rt = (Vout * Ro) / (Vin - Vout) 
    # Rt = 10000  # Used for Testing. Setting Rt=10k should give TempC=25
    
    # Steinhart - Hart Equation
    TempK = 1 / (A + (B * math.log(Rt)) + C * math.pow(math.log(Rt), 3))

    # Convert from Kelvin to Celsius
    TempC = TempK - 273.15

    print(round(TempC, 1))
    sleep(5)