#!/usr/bin/env python3
"""
Frio Mirror Tray App
System tray application for containerized Android screen mirroring.
Only works when connected to "Frio Fone" WiFi network.
"""

import os
import sys
import subprocess
import threading
import time
import json
from pathlib import Path

import pystray
from PIL import Image, ImageDraw

APP_NAME = "Frio Mirror"
TARGET_SSID = "Frio Fone"
CONTAINER_NAME = "frio-mirror"
ICON_SIZE = 64

# Track state
_mirror_running = False
_current_ssid = None


def get_wifi_ssid():
    """Get current WiFi SSID using nmcli."""
    try:
        result = subprocess.run(
            ["nmcli", "-t", "-f", "ACTIVE,SSID", "dev", "wifi"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if line.startswith('yes:'):
                    return line.split(':', 1)[1] if ':' in line else None
        return None
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
        print(f"Error getting WiFi SSID: {e}")
        return None


def is_on_frio_fone():
    """Check if connected to Frio Fone hotspot."""
    ssid = get_wifi_ssid()
    return ssid == TARGET_SSID


def is_mirror_running():
    """Check if the docker container is running."""
    try:
        result = subprocess.run(
            ["docker", "ps", "-q", "-f", f"name={CONTAINER_NAME}"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return bool(result.stdout.strip())
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def start_mirror():
    """Start the scrcpy docker container."""
    global _mirror_running
    
    # Check if on correct network
    if not is_on_frio_fone():
        print(f"Not connected to {TARGET_SSID}. Cannot start mirror.")
        return False
    
    # Check if already running
    if is_mirror_running():
        print("Mirror already running")
        return True
    
    # Kill any existing container first
    subprocess.run(
        ["docker", "rm", "-f", CONTAINER_NAME],
        capture_output=True,
        timeout=10
    )
    
    # Build if needed and run
    try:
        print("Starting Frio Mirror container...")
        env = os.environ.copy()
        env['DISPLAY'] = os.environ.get('DISPLAY', ':0')
        
        result = subprocess.run(
            ["docker", "compose", "up", "--build", "-d"],
            capture_output=True,
            text=True,
            timeout=120,
            env=env,
            cwd=str(Path(__file__).parent)
        )
        
        if result.returncode == 0:
            print("Mirror started successfully!")
            _mirror_running = True
            return True
        else:
            print(f"Failed to start: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("Timeout starting mirror")
        return False
    except Exception as e:
        print(f"Error starting mirror: {e}")
        return False


def stop_mirror():
    """Stop the scrcpy docker container."""
    global _mirror_running
    
    try:
        subprocess.run(
            ["docker", "compose", "down"],
            capture_output=True,
            timeout=30,
            cwd=str(Path(__file__).parent)
        )
        print("Mirror stopped")
        _mirror_running = False
        return True
    except Exception as e:
        print(f"Error stopping mirror: {e}")
        return False


def create_icon(color="blue"):
    """Create a simple phone icon."""
    width = ICON_SIZE
    height = ICON_SIZE
    
    # Color mapping
    colors = {
        "blue": (59, 130, 246),      # Available
        "green": (34, 197, 94),      # Connected/Mirroring
        "gray": (156, 163, 175),     # Not on network
    }
    
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    c = colors.get(color, colors["gray"])
    
    # Phone body (rectangle with rounded corners)
    margin = 8
    body_x1 = margin
    body_y1 = margin
    body_x2 = width - margin
    body_y2 = height - margin
    
    # Draw phone outline
    draw.rounded_rectangle(
        [body_x1, body_y1, body_x2, body_y2],
        radius=8,
        outline=c,
        width=4
    )
    
    # Screen area
    screen_margin = 14
    draw.rounded_rectangle(
        [body_x1 + screen_margin, body_y1 + screen_margin, 
         body_x2 - screen_margin, body_y2 - screen_margin],
        radius=4,
        fill=(*c, 50)
    )
    
    return img


def update_icon(icon):
    """Update tray icon based on state."""
    on_network = is_on_frio_fone()
    running = is_mirror_running()
    
    if running:
        icon.icon = create_icon("green")
        icon.title = f"{APP_NAME} - Mirroring Active"
    elif on_network:
        icon.icon = create_icon("blue")
        icon.title = f"{APP_NAME} - Ready (Frio Fone)"
    else:
        icon.icon = create_icon("gray")
        ssid = get_wifi_ssid() or "No WiFi"
        icon.title = f"{APP_NAME} - {ssid} (Connect to Frio Fone)"


def on_click_mirror(icon, item):
    """Handle mirror button click."""
    if not is_on_frio_fone():
        # Show notification or just log
        print(f"Not on {TARGET_SSID} network!")
        return
    
    if is_mirror_running():
        stop_mirror()
    else:
        # Run in thread to not block tray
        threading.Thread(target=start_mirror, daemon=True).start()
    
    # Update icon after a moment
    time.sleep(0.5)
    update_icon(icon)


def on_exit(icon, item):
    """Exit the application."""
    stop_mirror()
    icon.stop()
    sys.exit(0)


def create_menu(icon):
    """Create the tray menu."""
    on_network = is_on_frio_fone()
    running = is_mirror_running()
    
    ssid = get_wifi_ssid() or "Not connected"
    
    # Mirror action text
    if running:
        mirror_text = "⏹ Stop Mirror"
        mirror_enabled = True
    elif on_network:
        mirror_text = "▶ Start Mirror"
        mirror_enabled = True
    else:
        mirror_text = f"🔒 Start Mirror (Need {TARGET_SSID})"
        mirror_enabled = False
    
    status_text = f"📶 {ssid}"
    
    return pystray.Menu(
        pystray.MenuItem(status_text, lambda: None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(mirror_text, on_click_mirror, enabled=mirror_enabled),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("❌ Exit", on_exit)
    )


def background_update(icon):
    """Background thread to update icon periodically."""
    while True:
        time.sleep(5)
        try:
            update_icon(icon)
            icon.menu = create_menu(icon)
        except:
            pass


def main():
    """Main entry point."""
    print(f"Starting {APP_NAME}...")
    print(f"Target network: {TARGET_SSID}")
    
    # Check for Docker
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: Docker not found. Please install Docker.")
        sys.exit(1)
    
    # Check for nmcli
    try:
        subprocess.run(["nmcli", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("WARNING: nmcli not found. WiFi detection may not work.")
    
    # Create initial icon
    initial_icon = create_icon("gray")
    
    # Create the tray icon
    icon = pystray.Icon(
        APP_NAME.lower().replace(" ", "-"),
        initial_icon,
        title=APP_NAME,
        menu=create_menu
    )
    
    # Start background updater
    updater = threading.Thread(target=background_update, args=(icon,), daemon=True)
    updater.start()
    
    # Run
    icon.run()


if __name__ == "__main__":
    main()
