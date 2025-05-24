#!/bin/bash
set -e

# Copy script and service to image
install -m 755 files/register_device.py "${ROOTFS_DIR}/opt/device/register_device.py"
install -m 644 files/device-register.service "${ROOTFS_DIR}/etc/systemd/system/device-register.service"

on_chroot << EOF
systemctl enable device-register.service
EOF
