# Build container only (no tray app)
docker compose build

# Run container directly (bypass tray)
docker compose up

# Run full tray app
pip install -r requirements.txt
python tray_app.py

# Clean up
docker compose down
docker rm -f frio-mirror
