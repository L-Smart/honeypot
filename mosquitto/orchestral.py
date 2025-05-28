import subprocess
import time
import os
import signal
import json
from pathlib import Path

CONFIG_FILE = "devices/devices_config.json"

def load_devices():
    with open(CONFIG_FILE, "r") as f:
        devices = json.load(f)
    base_dir = Path(__file__).parent
    enabled_devices = []
    for d in devices:
        if d.get("enabled", False):
            script_path = base_dir / d["script"]
            if script_path.exists():
                enabled_devices.append(str(script_path))
            else:
                print(f"[WARNING] Script not found : {script_path}")
    print(f"[DEBUG] Devices loaded : {enabled_devices}")
    return enabled_devices

def main():
    devices = load_devices()
    processes = []

    try:
        for device in devices:
            print(f"[INFO] Launching {device}")
            try:
                p = subprocess.Popen(["python3", device])
                processes.append(p)
            except Exception as e:
                print(f"[ERROR] Can not launch {device} : {e}")

        print("[INFO] All the devices are launched, Ctrl+C to stop")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[INFO] Stopping the devices...")
        for p in processes:
            p.send_signal(signal.SIGINT)
        for p in processes:
            p.wait()
        print("[INFO] All the devices are stopped")

if __name__ == "__main__":
    main()