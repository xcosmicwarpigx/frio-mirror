#!/bin/bash
set -e

# Start ADB server as root first
adb start-server

# Check if wireless mode is enabled
if [ -n "$ADB_HOST" ]; then
    echo "Wireless mode enabled. Connecting to $ADB_HOST..."
    
    # If pairing code is provided, do pairing first
    if [ -n "$ADB_PAIRING_CODE" ] && [ -n "$ADB_PAIRING_PORT" ]; then
        echo "Pairing with device..."
        echo "$ADB_PAIRING_CODE" | adb pair "$ADB_HOST:$ADB_PAIRING_PORT" || true
    fi
    
    # Connect to the device
    echo "Connecting to $ADB_HOST:$ADB_PORT..."
    adb connect "$ADB_HOST:$ADB_PORT"
    
    # Wait for connection
    timeout=30
    while [ $timeout -gt 0 ]; do
        if adb devices | grep -q "$ADB_HOST"; then
            echo "Connected to wireless device!"
            break
        fi
        sleep 1
        ((timeout--))
    done
    
    if [ $timeout -eq 0 ]; then
        echo "Failed to connect to wireless device at $ADB_HOST:$ADB_PORT"
        echo "Make sure wireless debugging is enabled on your phone."
        echo "Available devices:"
        adb devices
        exit 1
    fi
else
    # USB Mode
    # Fix permissions for USB devices
    if [ -d /dev/bus/usb ]; then
        chmod -R 777 /dev/bus/usb 2>/dev/null || true
    fi

    # Wait for device with a timeout
    echo "Waiting for USB Android device..."
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
        echo "No USB device found within 30 seconds"
        echo "Available devices:"
        adb devices
        exit 1
    fi
fi

# Run scrcpy with the connected device
echo "Starting scrcpy..."
scrcpy \
    --window-title "Frio Mirror" \
    --window-borderless \
    --max-size 1920 \
    --max-fps 60 \
    2>&1
