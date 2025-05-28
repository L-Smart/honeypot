import paho.mqtt.client as mqtt
import time
import random
import socket

client_id = "door_sensor_1"
client = mqtt.Client(client_id=client_id)
client.connect("localhost", 1883, 60)
client.loop_start()

ip = socket.gethostbyname(socket.gethostname())
client.publish("honeypot/identication", f"{client_id}|{ip}")

while True:
    state = random.choice(["open", "closed"])
    client.publish("doors/1/status", state)
    time.sleep(10)