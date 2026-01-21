#! /bin/env bash
sudo apt update
sudo apt install -y mosquitto mosquitto-clients

pip install pyserial paho-mqtt