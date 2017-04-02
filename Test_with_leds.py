#This application is used to controll the pin 17 of the GPIO
#of the Raspberry Pi 3. It uses paho to comunicate to a mqtt broker



import RPi.GPIO as GPIO #import library to controll the GPIO of the RPi
import paho.mqtt.client as mqtt #import Library to communicate trough MQTT
import time #Library to be able to use the sleep function

#Configure the pins of the raspberry
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(12, GPIO.IN)
GPIO.setup(16, GPIO.IN)

# The callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    m="Connected flags"+str(flags)+"result code "\
    +str(rc)+"client1_id  "+str(client)
    print(m)

#The callback to receive and process messages
def on_message(client1, userdata, message):
    print("message received  "  ,str(message.payload.decode("utf-8")))
    state = str(message.payload.decode("utf-8")) # save on "state" the message 
    
    if (state == "1"):
        GPIO.output(17, GPIO.HIGH)

    else:
        GPIO.output(17, GPIO.LOW)



broker_address="192.168.0.232"

client1 = mqtt.Client("P1")         #Create a new instance
client1.on_connect = on_connect     #Attach function to a callback
client1.on_message=on_message       #attach function to callback
time.sleep(1)
client1.connect(broker_address)     #Connect to broker
client1.loop_start()               #start loop to process callbacks

client1.subscribe("led/rojo")   #Subscribe to the topic
#client1.subscribe("led/amarillo")
#client1.publish("led/rojo","OFF")
    


time.sleep(60)      #wait 1 minute 
GPIO.output(17, GPIO.LOW)   #turn doff the led 
client1.disconnect()    #Disconnect
client1.loop_stop()
