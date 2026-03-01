# Frio Mirror - Containerized Android Screen Mirroring

A Linux system tray application that mirrors your Android phone using scrcpy when connected to your "Frio Fone" hotspot.

## Features

- 🐧 Linux system tray icon
- 📶 WiFi network detection (only works on "Frio Fone")
- 📱 One-click Android screen mirroring via scrcpy
- 🐳 Fully containerized
- 🔄 Auto-detects USB-connected Android devices

## Requirements

- Linux with Docker
- Android phone with USB debugging enabled
- USB cable connection
- `nmcli` (NetworkManager) for WiFi detection

## Quick Start

```bash
# Build and run
docker compose up --build

# Or run the tray app directly (requires Python deps)
pip install -r requirements.txt
python tray_app.py
```

## Usage

1. Connect your Android phone via USB with debugging enabled
2. Make sure you're connected to the "Frio Fone" WiFi network
3. Click the tray icon and select "Mirror Phone"
4. Your phone screen will appear in a window

## Docker Permissions

The container needs:
- USB device access (`/dev/bus/usb`)
- X11 socket for GUI (`/tmp/.X11-unix`)
- Network detection capabilities

## License

MIT
