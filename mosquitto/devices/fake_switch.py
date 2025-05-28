import paho.mqtt.client as mqtt
import time
import socket

state = "OFF"
client_id = "fake_switch"
client = mqtt.Client(client_id)

def on_message(client, userdata, msg):
    global state
    payload = msg.payload.decode()
    if payload.upper() in ["ON", "OFF"]:
        state = payload.upper()
        print(f"Interrupteur état changé à {state}")
        client.publish("home/livingroom/light/status", state)

client.on_message = on_message
client.connect("localhost", 1883, 60)
client.subscribe("home/livingroom/light/set")


ip = socket.gethostbyname(socket.gethostname())
client.publish("honeypot/identification", f"{client_id}|{ip}")

client.loop_start()

try:
    while True:
        client.publish("home/livingroom/light/status", state)
        time.sleep(15)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()