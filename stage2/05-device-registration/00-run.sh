#!/bin/bash
set -e

INSTALL_DIR="/opt/device"
mkdir -p "$INSTALL_DIR"

# Copy script from pi-gen into the image
cp "$(dirname "$0")/register_device.py" "$INSTALL_DIR/"

# Set to execute on boot (via systemd)
cat > /etc/systemd/system/device-register.service <<EOF
[Unit]
Description=Device Auto Registration
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 $INSTALL_DIR/register_device.py
RemainAfterExit=true

[Install]
WantedBy=multi-user.target
EOF

systemctl enable device-register.service
