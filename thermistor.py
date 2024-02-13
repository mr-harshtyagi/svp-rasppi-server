from gpiozero import MCP3008
from time import sleep
import math

adc = MCP3008(channel=0)

# Voltage Divider
Vin = 3.3
Ro = 10000  # 10k Resistor

# Steinhart Constants
A = 0.001129148
B = 0.000234125
C = 0.0000000876741

while True:
    # Get Voltage value from ADC   
    Vout = adc.value * Vin
    
    # Calculate Resistance
    Rt = (Vout * Ro) / (Vin - Vout) 
    
    # Steinhart - Hart Equation
    TempK = 1 / (A + (B * math.log(Rt)) + C * math.pow(math.log(Rt), 3))

    # Convert from Kelvin to Celsius
    TempC = TempK - 273.15

    print(round(TempC, 1))
    sleep(5)