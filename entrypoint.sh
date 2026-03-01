#!/bin/bash
set -e

# Start ADB server as root first
adb start-server

# Fix permissions for USB devices
if [ -d /dev/bus/usb ]; then
    chmod -R 777 /dev/bus/usb 2>/dev/null || true
fi

# Wait for device with a timeout
echo "Waiting for Android device..."
timeout=30
while [ $timeout -gt 0 ]; do
    if adb devices | grep -q "device$"; then
        echo "Device found!"
        break
    fi
    sleep 1
    ((timeout--))
done

if [ $timeout -eq 0 ]; then
    echo "No device found within 30 seconds"
    echo "Available devices:"
    adb devices
    exit 1
fi

# Run scrcpy with the connected device
echo "Starting scrcpy..."
scrcpy \
    --window-title "Frio Mirror" \
    --window-borderless \
    --max-size 1920 \
    --max-fps 60 \
    --encoder 'OMX.google.h264.encoder' \
    2>&1
