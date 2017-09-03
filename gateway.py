import datetime
import json
import time
import os

import paho.mqtt.client as mqtt
from RFM69.RFM69 import RFM69
from RFM69.RFM69registers import *

RFM_NODE = 1
RFM_NETWORK = 100
RFM_PI_INTERRUPT_PIN = 22
RFM_IS_HIGH_POWER = True #Set this to false if not using the high power version

# Get the Losant and RFM configuration from environment variables
losant_device_id = None
losant_key = None
losant_secret = None
rfm_encrypt_key = None

try:
  losant_device_id = os.environ["LOSANT_DEVICE_ID"]
  losant_key = os.environ["LOSANT_KEY"]
  losant_secret = os.environ["LOSANT_SECRET"]
  rfm_encrypt_key = os.environ["RFM_ENCRYPT_KEY"]
except KeyError as e:
  print('Environment variable not found: {}'.format(e.message))
  print("You need to define the environment variables LOSANT_DEVICE_ID, "
        "LOSANT_KEY, LOSANT_SECRET and RFM_ENCRYPT_KEY")
  exit(-1)

# Configure the RFM69 module
radio = RFM69(RF69_433MHZ, 
                    RFM_NODE, 
                    RFM_NETWORK, 
                    RFM_IS_HIGH_POWER, 
                    intPin=RFM_PI_INTERRUPT_PIN)

if RFM_IS_HIGH_POWER:
  radio.setHighPower(True)

radio.encrypt(rfm_encrypt_key)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

# Configure the MQTT client to connect to Losant
client = mqtt.Client(client_id=losant_device_id)
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(losant_key, losant_secret)
client.connect("broker.losant.com", 1883, 60)
client.loop_start();

try:
  # Loop until Ctrl-C
  while True:
    radio.receiveBegin()
    while not radio.receiveDone():
      time.sleep(0.1)

    # Extract the JSON from the RFM data payload
    json_str = ''.join([chr(byte_val) for byte_val in radio.DATA])
    data = json.loads(json_str)
    print('{} - RSSI:{}'.format(data, radio.RSSI))

    radio.sendACK()

    # Forward the message to the topic specified in the JSON
    client.publish(data["topic"], data["msg"])
    time.sleep(1)
except KeyboardInterrupt:
  radio.shutdown()
  client.loop_stop()
