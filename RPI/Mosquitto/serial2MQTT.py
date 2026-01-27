#! /bin/env python3
from gpiozero import LED
import argparse
import serial
import time
import sys
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish


lightOK = LED(19)
lightWARN = LED(16)
lightCRIT = LED(13)

totalOK = LED(26)
totalWARN = LED(21)
totalCRIT = LED(20)

# LED Test
totalOK.on()
totalWARN.on()
totalCRIT.on()
lightOK.on()
lightWARN.on()
lightCRIT.on()
time.sleep(5)
totalOK.off()
totalWARN.off()
totalCRIT.off()
lightOK.off()
lightWARN.off()
lightCRIT.off()

parser = argparse.ArgumentParser(description="Arduino to MQTT Script")
parser.add_argument("--broker", default="localhost", help="MQTT broker IP address")
parser.add_argument("--port", default=1883, help="MQTT broker port")
parser.add_argument("--user", help="MQTT broker User")
parser.add_argument("--pass", dest="password", help="MQTT broker Password")
parser.add_argument("--serial", default="/dev/ttyACM0", help="Arduino serial port")
args = parser.parse_args()
SERIAL_PORT = args.serial
BAUD_RATE = 9600
MQTT_BROKER = args.broker
MQTT_PORT = args.port
mqtt_auth = {
    "username": args.user,
    "password": args.password
}
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_start()
state = [0,0,0]
unit = int(500)
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)
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
            totalOK.on()
            totalWARN.off()
            totalCRIT.off()
        elif worststate == 1:
            totalOK.off()
            totalWARN.on()
            totalCRIT.off()
        elif worststate ==2:
            totalOK.off()
            totalWARN.off()
            totalCRIT.on()

        if state[1] == 0:
            lightOK.on()
            lightWARN.off()
            lightCRIT.off()
        elif state[1] == 1:
            lightOK.off()
            lightWARN.on()
            lightCRIT.off()
        elif state[1] ==2:
            lightOK.off()
            lightWARN.off()
            lightCRIT.on()

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
