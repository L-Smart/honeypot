import paho.mqtt.client as mqtt
import time
import random
import socket

client_id = "temp_sensor_1"
client = mqtt.Client(client_id)
client.connect("localhost", 1883, 60)

ip = socket.gethostbyname(socket.gethostname())
client.publish("honeypot/identification", f"{client_id}|{ip}")

while True:
    temp = round(random.uniform(20, 30), 2)
    client.publish("sensors/temp1", f"{temp}")
    time.sleep(5)