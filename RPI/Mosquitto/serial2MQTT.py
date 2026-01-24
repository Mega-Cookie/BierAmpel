#! /bin/env python3
import serial
import time
import sys
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600
MQTT_BROKER = "fs2clf7.lab"
mqtt_auth = {
    'username': "your_username",
    'password': "your_password"
}
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(MQTT_BROKER, 1883)
client.loop_start()
state = [0,0,0]
unit = int(500)
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)
while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        data = line.split(',')
        data = [float(item.split(":")[1]) for item in data]
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
        msgs = [
            {'topic': "bierampel/weight/sensor", 'payload': data[0]},
            {'topic': "bierampel/weight/count", 'payload': count},
            {'topic': "bierampel/weight/state", 'payload': state[0]},
            {'topic': "bierampel/light/sensor", 'payload': data[1]},
            {'topic': "bierampel/light/alarm", 'payload': data[2]},
            {'topic': "bierampel/light/state", 'payload': state[1]},
            {'topic': "bierampel/temp/sensor", 'payload': data[3]},
            {'topic': "bierampel/temp/state", 'payload': state[2]},
            {'topic': "bierampel/total/state", 'payload': worststate}
        ]
        publish.multiple(msgs, hostname=MQTT_BROKER)

        if worststate == 0:
            print("OK! Lecker Bierchen ist bereit.|Temperatur:" + data[3] + ";15,20;; Dosen:" + count + ";2;1;;")
            sys.exit(0)
        elif worststate == 1:
            print("WARNING! Die Wahrscheinlichkeit für lecker Bierchen is gering, aber nie Null.|Temperatur:" + data[3] + ";15,20;; Dosen:" + count + ";2;1;;")
            sys.exit(1)
        elif worststate == 2 and count == 0:
            print("CRITICAL! Kein Bierchen.|Temperatur:" + data[3] + ";15,20;; Dosen:" + count + ";2;1;;")
            sys.exit(2)
        elif worststate == 2 and state[1] == 2:
            print("CRITICAL! Lecker Bierchen ist in Gefahr.|Temperatur:" + data[3] + ";15,20;; Dosen:" + count + ";2;1;;")
            sys.exit(2)
        elif worststate == 2 and state[2] == 2:
            print("CRITICAL! Lecker Bierchen ist zu Warm.|Temperatur:" + data[3] + ";15,20;; Dosen:" + count + ";2;1;;")
            sys.exit(2)
