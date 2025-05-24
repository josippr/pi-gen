#!/usr/bin/env python3

import os
import json
import uuid
import requests
import datetime
import jwt
import time

# TODO: Replace with acutal secret

CONFIG_PATH = "/opt/device/config.json"
API_URL = "https://lms-stage.josip-prpic.from.hr/api/register-device"
JWT_SECRET = "xxxxx"

def get_mac():
    mac = open('/sys/class/net/eth0/address').read().strip()
    return mac.lower()

def generate_serial(mac):
    mac_suffix = mac.replace(":", "")[-6:]
    dt_str = time.strftime("%y%m-%H-%M")
    serial = f"lms-proto-t1-{mac_suffix}-{dt_str}"
    name = f"lms-proto-t1-{mac_suffix}"
    return serial, name, mac

def generate_jwt():
    payload = {
        "sub": "proto-device",
        "scope": "device:register",
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=90)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def register_device(config):
    headers = {"Authorization": f"Bearer {config['jwt_token']}"}
    res = requests.post(API_URL, headers=headers, json=config)
    print("API Response:", res.status_code, res.text)

def main():
    serial, name, mac = generate_serial(get_mac())
    jwt_token = generate_jwt()

    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
    except:
        config = {}

    config.update({
        "serial_number": serial,
        "device_name": name,
        "mac_address": mac,
        "datetime_registered": datetime.datetime.utcnow().isoformat() + "Z",
        "jwt_token": jwt_token
    })

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

    register_device(config)

if __name__ == "__main__":
    main()
