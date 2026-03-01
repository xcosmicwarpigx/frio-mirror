FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install only essential packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    scrcpy \
    adb \
    libgl1 \
    libglx-mesa0 \
    libsdl2-2.0-0 \
    usbutils \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 5037

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
