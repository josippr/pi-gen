#!/bin/bash
set -e

CONFIG_DIR="/etc/device"
mkdir -p "$CONFIG_DIR"

# install python3 if not already installed and python3-requests for HTTP requests
if ! command -v python3 &> /dev/null; then
    apt-get update
    apt-get install -y python3 python3-requests
fi

# Generate MAC address hash
MAC=$(cat /sys/class/net/eth0/address | tr -d ':' | cut -c 7-12)
DATE_ID=$(date +"%y%m-%H-%M")
SERIAL="lms-proto-t1-${MAC}-${DATE_ID}"
DEVICENAME="lms-proto-t1-${MAC}"

# Generate token
TOKEN=$(openssl rand -hex 32)

cat > "${CONFIG_DIR}/device.conf" <<EOF
serial=${SERIAL}
deviceName=${DEVICENAME}
owner=
registered=false
registeredAt=
license=
lastSeen=
token=${TOKEN}
EOF
