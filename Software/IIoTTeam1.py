#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cayenne.client
import time
import logging
import RPi.GPIO as GPIO
import time
import time, sys
import Adafruit_DHT
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
from gpiozero import LED
from time import sleep
relay = LED(18)

username = "7cb0a840-21b9-11ea-84bb-8f71124cfdfb"
password = "5fb0e1032342ead439ac9892b588a96969c7a462"
clientid = "cc8b53c0-21bd-11ea-b301-fd142d6c1e6c"

##DHT22
sensor = Adafruit_DHT.DHT22
pin = 4  #GPIO4
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

##MQ135
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#moisture
channel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

#relay
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
RELAIS_1_GPIO = 18
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT)
 

mqttc = mqtt.Client(client_id=clientid)
mqttc.username_pw_set(username, password=password)
mqttc.connect("mqtt.mydevices.com", port=1883, keepalive=60)
mqttc.loop_start()

temp_value = "v1/" + username + "/things/" + clientid + "/data/1"
humidity_value = "v1/" + username + "/things/" + clientid + "/data/2"
temp_graph = "v1/" + username + "/things/" + clientid + "/data/3"
air_value = "v1/" + username + "/things/" + clientid + "/data/4"
moisture_value = "v1/" + username + "/things/" + clientid + "/data/5"
humidity_g = "v1/" + username + "/things/" + clientid + "/data/6"


while True:

    try:
        ##DHT22
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        if temperature is not None:

            temperature = "temp,c=" + str(temperature)

            mqttc.publish(temp_value, payload=temperature, retain=True)
            mqttc.publish(temp_graph, payload=temperature, retain=True)

        if humidity is not None:

            humidity = "rel_hum,p=" + str(humidity)

            mqttc.publish(humidity_value, payload=humidity, retain=True)
            mqttc.publish(humidity_g, payload=humidity, retain=True)
            
               
        ##MQ135
        def action(pin):
            print ('Danger!')
            print (str(GPIO.input(16)))
            Airquality = "prox,d=" + str(GPIO.input(16))
            relay.on()
            mqttc.publish(air_value, payload=Airquality, retain=True)
            return

        try:
            while True:
                print ('Safe.')
                print (str(GPIO.input(16)))
                Airquality = "prox,d=" + str(GPIO.input(16))
                relay.off()                              
                mqttc.publish(air_value, payload=Airquality, retain=True)
                time.sleep(1)
                break            
            
        except KeyboardInterrupt:
            GPIO.cleanup()
        
        #moisture

        while True:
                if GPIO.input(channel) == GPIO.HIGH:                    
                        print ("dry")
                        print (str(GPIO.input(channel)))
                        moisture = "prox,d=" + str(0)
                        relay.on()
                        mqttc.publish(moisture_value, payload=moisture, retain=True)
                else :                    
                        print ("wet")
                        print (str(GPIO.input(channel)))
                        relay.off()
                        moisture = "prox,d=" + str(1)
                        mqttc.publish(moisture_value, payload=moisture, retain=True)                        

                time.sleep(1)
                break
                
      
    except (EOFError, SystemExit, KeyboardInterrupt):
        mqttc.disconnect()
        sys.exit()