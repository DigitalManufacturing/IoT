#!/usr/bin/python

# Description          Neoris - Digital Manufacturing - Internet of things
# Author               David Palavecino - david.palavecino@neoris.com
# Connectivity         Raspberry Pi3 > MHT11 Sensor > MQTT  
#
 
# Libs Import
import sys
import time
import json
import Adafruit_DHT
import paho.mqtt.client as mqtt

# Broker Connection Info
brokerURL = "192.168.1.118"
brokerPort = "1883"

# DHT Sensor Type
sensor = Adafruit_DHT.DHT11

# Configuracion del puerto GPIO al cual esta conectado  (GPIO 23)
pin = 23

def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("$SYS/#")
    
def on_message(client, userdata, msg):
    print(msg.topic+ " " + str(msg.payload))
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(brokerURL, brokerPort, 60)

# Try & Exceptions Control
try:	
	# LOOP
	while True:
		# get Sensor Values
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		
		# MQTT_TEMPERATURE_MSG = json.dumps({"TEMPERATURE": '{0:0.1f}'.format(temperature, humidity)})
		# MQTT_HUMIDITY_MSG = json.dumps({"HUMIDITY": '{1:0.1f}'.format(temperature, humidity)})
        	MQTT_FULL_MSG = json.dumps({"capabilityAlternateId": "IG_5B460280D08201081600C406F02CBA47", "sensorAlternateId":"fc32d1702c14820e","I_NE_CL_RaspberryTemperature": '{0:0.1f}'.format(temperature, humidity), "I_NE_CL_RaspberryHumidity": '{1:0.1f}'.format(temperature, humidity)})

		# Print temperature y humidity with 1 decimal
                #	print('Temperature={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))

                # Message Sending
                MSG_FULL = client.publish("neoris/sensors/cl", MQTT_FULL_MSG)
               
                print(MQTT_FULL_MSG)    

		# sleep 1 sec
		time.sleep(10)

# Exceptions
except Exception,e:
	# Imprime en pantalla el error e
	print str(e)
