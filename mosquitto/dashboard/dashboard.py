import streamlit as st
from pathlib import Path
import json
import re
from streamlit_autorefresh import st_autorefresh

LOG_FILE = Path(__file__).parent.parent / "mqtt_log.json"
MOSQUITTO_LOG_FILE = Path("/var/log/mosquitto/mosquitto.log")

st.title("MQTT Honeypot Dashboard")

count = st_autorefresh(interval=2000, limit=100, key="mqtt_log_autorefresh")

def read_last_logs(n=50):
    if not LOG_FILE.exists():
        return []
    logs = []
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()[-n:]
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                log = json.loads(line)
                logs.append(log)
            except json.JSONDecodeError:
                st.warning(f"Invalid JSON line: {line}")
    return logs

logs = read_last_logs(50)

st.subheader("Last MQTT messages:")
if logs:
    for log in reversed(logs):
        st.write(f"**{log['timestamp']}** — `{log['topic']}` — `{log['payload']}` — Client: `{log['client_id']}` — IP: `{log['ip']}`")
else:
    st.write("No MQTT messages available.")