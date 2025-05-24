#!/bin/bash
set -e

install -d "${ROOTFS_DIR}/opt/device"
cat > "${ROOTFS_DIR}/opt/device/config.json" <<EOF
{
  "firmware_version": "1.0.0",
  "batch_version": "batch-001"
}
EOF
