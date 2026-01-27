#! /bin/env python3
from gpiozero import LED
import argparse
import serial
import time
import sys
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# Define LED Pins
leds = LEDBoard(
    lightOK = 17,
    lightWARN = 16,
    lightCRIT = 13,
    weightOK = 12,
    weightWARN = 6,
    weightCRIT = 5,
    lightOK = 12,
    lightWARN = 6,
    lightCRIT = 5
)

# LED Test
leds.on()
sleep(3)
leds.off()

for led in leds:
    led.on()
    sleep(0.5)
    led.off()

# Input arguments
parser = argparse.ArgumentParser(description="Arduino to MQTT Script")

parser.add_argument("--serial", default="/dev/ttyACM0", help="Arduino serial port")
parser.add_argument("--baud", default=9600, help="Serial Baud rate")

parser.add_argument("--broker", default="localhost", help="MQTT broker IP address")
parser.add_argument("--port", default=1883, help="MQTT broker port")
parser.add_argument("--user", help="MQTT broker User")
parser.add_argument("--pass", dest="password", help="MQTT broker Password")

args = parser.parse_args()

SERIAL_PORT = args.serial
BAUD_RATE = args.baud

MQTT_BROKER = args.broker
MQTT_PORT = args.port
mqtt_auth = {
    "username": args.user,
    "password": args.password
}
# Connect to MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_start()

state = [0,0,0]
unit = int(500)

# Connect to Serial
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

# Read Sensors, Switch LEDs, Send MQTT
while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode("utf-8").strip()
        data = line.split(",")
        data = [float(item.split(":")[1]) for item in data]
        data = [int(v) if v.is_integer() else v for v in data]
        count = data[0]/unit
        if count <= 2:
            if count < 1:
                state[0] = 2
            else:
                state[0] = 1
        else:
            state[0] = 0

        if data[1] == 1:
            state[1] = 1
        else:
            state[1] = 0

        if data[3] > 15:
            if data[3] > 20:
                state[2] = 2
            else:
                state[2] = 1
        else:
            state[2] = 0
        if data[2] == 1:
            for i in range(len(state)):
                state[i] = 2
        state[0] = 0 # placeholder state
        state[2] = 0 # placeholder state
        worststate = max(state)
        if worststate == 0:
            leds.totalOK.on()
            leds.totalWARN.off()
            leds.totalCRIT.off()
        elif worststate == 1:
            leds.totalOK.off()
            leds.totalWARN.on()
            leds.totalCRIT.off()
        elif worststate ==2:
            leds.totalOK.off()
            leds.totalWARN.off()
            leds.totalCRIT.on()

        if state[1] == 0:
            leds.lightOK.on()
            leds.lightWARN.off()
            leds.lightCRIT.off()
        elif state[1] == 1:
            leds.lightOK.off()
            leds.lightWARN.on()
            leds.lightCRIT.off()
        elif state[1] ==2:
            leds.lightOK.off()
            leds.lightWARN.off()
            leds.lightCRIT.on()

        msgs = [
            {"topic": "bierampel/weight/sensor", "payload": data[0]},
            {"topic": "bierampel/weight/count", "payload": count},
            {"topic": "bierampel/weight/state", "payload": state[0]},
            {"topic": "bierampel/light/sensor", "payload": data[1]},
            {"topic": "bierampel/light/alarm", "payload": data[2]},
            {"topic": "bierampel/light/state", "payload": state[1]},
            {"topic": "bierampel/temp/sensor", "payload": data[3]},
            {"topic": "bierampel/temp/state", "payload": state[2]},
            {"topic": "bierampel/worst/state", "payload": worststate}
        ]
        publish.multiple(msgs, hostname=MQTT_BROKER)
