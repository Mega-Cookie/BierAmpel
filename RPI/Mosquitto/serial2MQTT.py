import serial
import paho.mqtt.client as mqtt

# 1. Setup Serial connection (match Arduino baud rate)
# Identify port using 'ls /dev/tty*' in terminal
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# 2. Setup MQTT client
client = mqtt.Client()
client.connect("localhost", 1883, 60) # Connects to the Pi's local broker

while True:
    if ser.in_waiting > 0:
        # Read a line from Arduino and decode it
        line = ser.readline().decode('utf-8').strip()
        
        if line:
            print(f"Relaying: {line}")
            # Publish to a topic
            client.publish("arduino/sensor", line)