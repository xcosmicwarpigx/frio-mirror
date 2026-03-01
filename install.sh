#!/bin/bash
# Frio Mirror - Quick Install Script for Linux

set -e

echo "🚗 Frio Mirror Installer"
echo "========================"

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first:"
    echo "   https://docs.docker.com/engine/install/"
    exit 1
fi

# Check for nmcli (NetworkManager)
if ! command -v nmcli &> /dev/null; then
    echo "⚠️  nmcli not found. WiFi network detection may not work."
    echo "   Install NetworkManager for full functionality."
fi

# Check for Docker permissions
if ! docker ps &> /dev/null; then
    echo "⚠️  Docker permission issue. You may need to:"
    echo "   sudo usermod -aG docker $USER"
    echo "   Then log out and back in."
fi

echo ""
echo "📦 Building Docker container..."
docker build -t frio-mirror:latest .

echo ""
echo "🐍 Installing Python dependencies..."
pip3 install --user -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "To start Frio Mirror, run:"
echo "   python3 tray_app.py"
echo ""
echo "Make sure:"
echo "   1. Your Android phone has USB debugging enabled"
echo "   2. You're connected to 'Frio Fone' WiFi"
echo "   3. Your phone is plugged in via USB"
