import requests
import json
from datetime import datetime

CONFIG_PATH = "/etc/device/device.conf"
API_ENDPOINT = "https://lms-stage.josip-prpic.from.hr/api/register-device"

def parse_config():
    with open(CONFIG_PATH, "r") as f:
        lines = f.readlines()
    return {line.split("=")[0]: line.strip().split("=")[1] for line in lines if "=" in line}

def save_config(data):
    with open(CONFIG_PATH, "w") as f:
        for key, value in data.items():
            f.write(f"{key}={value}\n")

def main():
    config = parse_config()

    if config.get("registered") == "true":
        return  # Already registered

    payload = {
        "serial": config["serial"],
        "deviceName": config["deviceName"],
        "token": config.get("token", "")
    }

    try:
        res = requests.post(API_ENDPOINT, json=payload)
        if res.status_code == 200:
            data = res.json()
            config.update({
                "owner": data.get("owner", ""),
                "registered": "true",
                "registeredAt": datetime.utcnow().isoformat(),
                "license": data.get("license", ""),
                "lastSeen": datetime.utcnow().isoformat()
            })
            save_config(config)
    except Exception as e:
        print("Registration failed:", e)

if __name__ == "__main__":
    main()
