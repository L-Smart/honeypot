import paho.mqtt.client as mqtt
import json
from datetime import datetime
from pathlib import Path
import re

LOG_FILE = "mqtt_log.json"
MOSQUITTO_LOG_FILE = "/var/log/mosquitto/mosquitto.log"

known_clients = {}

def get_client_ip_map(log_path=MOSQUITTO_LOG_FILE):
    client_ips = {}
    if not Path(log_path).exists():
        return client_ips

    with open(log_path) as f:
        for line in f:
            m = re.search(r"New client connected from (\S+) as (\S+)", line)
            if m:
                ip, client_id = m.groups()
                client_ips[client_id] = ip
    return client_ips

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[INFO] Connected to MQTT broker")
        client.subscribe("#")
    else:
        print(f"[ERROR] Connection failure, return code : {rc}")

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"[INFO] Subscribed with QoS {granted_qos}")

def on_message(client, userdata, msg):
    global known_clients

    topic = msg.topic
    payload = msg.payload.decode()

    if topic == "honeypot/identification":
        if "|" in payload:
            client_id, ip = payload.split("|", 1)
            known_clients[client_id] = ip
            print(f"[INFO] Identication received : {client_id} à {ip}")
        return


    client_id = topic.split("/")[0]
    ip = known_clients.get(client_id, userdata.get("client_ips", {}).get(client_id, "127.0.0.1"))

    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "topic": topic,
        "payload": payload,
        "client_id": client_id,
        "ip": ip,
        "qos": msg.qos
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log) + "\n")

    print(f"[LOG] {log}")


client_ips = get_client_ip_map()


client = mqtt.Client("logger", userdata={"client_ips": client_ips})
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()