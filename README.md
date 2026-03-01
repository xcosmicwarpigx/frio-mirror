# Frio Mirror - Containerized Android Screen Mirroring

A Linux system tray application that mirrors your Android phone using scrcpy when connected to your "Frio Fone" hotspot.

## Features

- 🐧 Linux system tray icon
- 📶 WiFi network detection (only works on "Frio Fone")
- 📱 **USB Mode:** One-click Android screen mirroring via USB
- 📡 **Wireless Mode:** Mirror over WiFi (Android 11+ required)
- 🐳 Fully containerized
- 🔄 Auto-detects connected Android devices

## Requirements

- Linux with Docker
- Android phone with debugging enabled:
  - **USB Mode:** USB debugging enabled
  - **Wireless Mode:** Wireless debugging enabled (Android 11+)
- `nmcli` (NetworkManager) for WiFi detection
- For wireless: Must be connected to "Frio Fone" WiFi

## Quick Start

```bash
# Clone and install
git clone https://github.com/xcosmicwarpigx/frio-mirror.git
cd frio-mirror
./install.sh

# Run the tray app
python3 tray_app.py
```

## Usage

### USB Mode (Default)

1. Enable **USB debugging** on your Android phone (Settings → Developer Options)
2. Connect your phone via USB
3. Click the tray icon and select "Start Mirror (USB)"

### Wireless Mode

Requires Android 11 or higher.

1. Enable **Wireless debugging** on your phone:
   - Settings → Developer Options → Wireless debugging → Enable
   - Note the IP address and port shown
2. In Frio Mirror, switch to Wireless Mode:
   - Right-click tray icon → "Mode: Wireless"
   - Set your phone's IP address
3. Make sure you're connected to "Frio Fone" WiFi
4. Click "Start Mirror (Wireless)"

**First-time pairing:**
- On your phone, tap "Pair device with pairing code"
- Enter the pairing code when prompted

## Tray Icon Colors

| Color | Meaning |
|-------|---------|
| Gray | Wrong WiFi (wireless) or no USB device connected |
| Blue | USB mode ready |
| Purple | Wireless mode ready (Frio Fone) |
| Green | Mirroring active |

## Configuration

Settings are stored in `~/.config/frio-mirror/config.json`:

```json
{
  "wireless_mode": true,
  "phone_ip": "192.168.1.123"
}
```

## Docker Permissions

The container needs:
- USB device access for USB mode (`/dev/bus/usb`)
- X11 socket for GUI (`/tmp/.X11-unix`)
- Network access for wireless mode (`network_mode: host`)

## Troubleshooting

**"No device found" (USB mode):**
- Make sure USB debugging is enabled on your phone
- Try a different USB cable (some cables are charge-only)
- Run `adb devices` on host to check if device appears

**"Failed to connect" (Wireless mode):**
- Verify you're on "Frio Fone" WiFi
- Check the IP address matches your phone's wireless debugging IP
- Ensure wireless debugging is still enabled on your phone
- Firewall may be blocking port 5555

**Docker permission denied:**
```bash
sudo usermod -aG docker $USER
# Log out and back in
```

## License

MIT
