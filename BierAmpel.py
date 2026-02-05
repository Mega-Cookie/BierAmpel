#! /bin/env python3
from gpiozero import LEDBoard, Device
from gpiozero.pins.lgpio import LGPIOFactory
import argparse
import serial
from time import sleep
import sys
import signal
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

Device.pin_factory = LGPIOFactory()

def cleanup_and_exit(sig, frame):
    print("\nBeende Binary sauber...")
    
    # 1. LEDs abschalten
    leds.close() # Explizites Schließen
    print("LEDs abgschalten.")

    # 2. MQTT sauber trennen
    client.loop_stop()
    client.disconnect()
    print("MQTT-Verbindung getrennt.")
    
    # 3. Seriellen Port schließen
    if ser.is_open:
        ser.close()
    print("Serielle Schnittstelle geschlossen.")
    
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup_and_exit)
signal.signal(signal.SIGTERM, cleanup_and_exit)

def ledswitch(sensor, state):
    state_map = {0: "OK", 1: "WARN", 2: "CRIT"}
    suffix = state_map.get(state)
    if suffix:
        sensor_name = f"{sensor}{suffix}"
        led_obj = getattr(leds, sensor_name)
        led_obj.on()
        print(sensor_name)

# Define LED Pins
sensor_state_map = {0: "weight", 1: "light", 2: "temp", 3: "env", 4: "total"}
led_order = [
    'totalOK', 'totalWARN', 'totalCRIT',
    'lightOK', 'lightWARN', 'lightCRIT',
    'weightOK', 'weightWARN', 'weightCRIT',
    'tempOK', 'tempWARN', 'tempCRIT',
    'envOK', 'envWARN', 'envCRIT'
]
leds = LEDBoard(
    totalOK = 26,
    totalWARN = 21,
    totalCRIT = 20,
    lightOK = 19,
    lightWARN = 16,
    lightCRIT = 13,
    weightOK = 12,
    weightWARN = 6,
    weightCRIT = 5,
    tempOK = 27,
    tempWARN = 22,
    tempCRIT= 17,
    envWARN = 24,
    envOK = 25,
    envCRIT = 23
)

# LED Test
# all
leds.on()
sleep(3)
leds.off()
sleep(0.5)
# cycle
for name in led_order:
    led = getattr(leds, name)
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

state = [0,0,0,0,0]
unit = int(500)

# Connect to Serial
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
sleep(2)

# Read Sensors, Switch LEDs, Send MQTT
try:
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
            state[4] = max(state[0:4])

            for led in leds:
                led.off()

            for i in range(0,5,1):
                ledswitch(sensor_state_map.get(i), state[i])

            msgs = [
                {"topic": "bierampel/weight/sensor", "payload": data[0]},
                {"topic": "bierampel/weight/count", "payload": count},
                {"topic": "bierampel/weight/state", "payload": state[0]},
                {"topic": "bierampel/light/sensor", "payload": data[1]},
                {"topic": "bierampel/light/alarm", "payload": data[2]},
                {"topic": "bierampel/light/state", "payload": state[1]},
                {"topic": "bierampel/temp/sensor", "payload": data[3]},
                {"topic": "bierampel/temp/state", "payload": state[2]},
                {"topic": "bierampel/worst/state", "payload": state[4]}
            ]
            publish.multiple(msgs, hostname=MQTT_BROKER)
except Exception as e:
    print(f"Fehler: {e}")
    cleanup_and_exit(None, None)