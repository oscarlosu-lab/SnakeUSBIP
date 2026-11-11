#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# SnakeUSBIP Server for Linux & Raspberry Pi - 1-Click Installer
# Copyright (c) 2025-2026 oscarlosu-lab - https://github.com/oscarlosu-lab/SnakeUSBIP-Server
# Licensed under GPL v3
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║     🌐 SnakeUSBIP Server for Linux / Raspberry Pi Installer         ║${NC}"
echo -e "${CYAN}║            Universal Control Suite & 1-Click Auto-Setup              ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════════╝${NC}"

if [ "${EUID:-$(id -u)}" -ne 0 ]; then
    echo -e "${RED}[✗] Please run as root (use sudo).${NC}"
    exit 1
fi

echo -e "${BLUE}[1/5] Detecting package manager & installing dependencies...${NC}"
if command -v apt-get &> /dev/null; then
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -qq || true
    if ! apt-get install -y -qq usbip hwdata usbutils python3 avahi-daemon libnss-mdns 2>/dev/null; then
        apt-get install -y -qq "linux-tools-$(uname -r)" linux-tools-generic hwdata usbutils python3 avahi-daemon libnss-mdns 2>/dev/null || \
        apt-get install -y -qq usbip hwdata usbutils python3 avahi-daemon libnss-mdns 2>/dev/null || true
    fi
elif command -v dnf &> /dev/null; then
    dnf install -y -q usbip hwdata usbutils python3 avahi || true
elif command -v pacman &> /dev/null; then
    pacman -Sy --noconfirm usbip hwdata usbutils python avahi || true
else
    echo -e "${YELLOW}[!] Unknown package manager. Please ensure 'usbip', 'usbutils' and 'python3' are installed.${NC}"
fi

# Fallback linking for Ubuntu linux-tools kernel wrapper mismatch
if ! command -v usbipd &> /dev/null; then
    actual_usbipd=$(find /usr/lib/linux-tools /usr/lib/modules -name usbipd -type f 2>/dev/null | sort -V | tail -n 1 || true)
    if [ -n "$actual_usbipd" ]; then
        mkdir -p /usr/local/sbin
        ln -sf "$actual_usbipd" /usr/local/sbin/usbipd
        actual_usbip=$(dirname "$actual_usbipd")/usbip
        [ -f "$actual_usbip" ] && ln -sf "$actual_usbip" /usr/local/sbin/usbip
    fi
fi

echo -e "${BLUE}[2/5] Loading USB/IP kernel modules...${NC}"
modprobe usbip_core 2>/dev/null || true
modprobe usbip_host 2>/dev/null || true

# Persist modules across reboot
mkdir -p /etc/modules-load.d
cat << 'EOF' > /etc/modules-load.d/usbip.conf
usbip_core
usbip_host
EOF

# Find resolved usbipd executable path
USBIPD_BIN=$(command -v usbipd || which usbipd || echo "/usr/sbin/usbipd")

echo -e "${BLUE}[3/5] Installing systemd background service (usbipd.service)...${NC}"
cat << EOF > /etc/systemd/system/usbipd.service
[Unit]
Description=SnakeUSBIP USB/IP Server Daemon
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
Environment=PYTHONUNBUFFERED=1
ExecStart=${USBIPD_BIN} -4
Restart=always
RestartSec=3
KillMode=process

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable usbipd
systemctl restart usbipd

echo -e "${BLUE}[4/5] Installing unified Control Suite (snakeusbip-ctl)...${NC}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/snakeusbip-ctl" ]; then
    cp "$SCRIPT_DIR/snakeusbip-ctl" /usr/local/bin/snakeusbip-ctl
    chmod +x /usr/local/bin/snakeusbip-ctl
else
    # Download latest if running via curl pipe
    curl -fsSL https://raw.githubusercontent.com/oscarlosu-lab/SnakeUSBIP/main/scripts/snakeusbip-ctl -o /usr/local/bin/snakeusbip-ctl
    chmod +x /usr/local/bin/snakeusbip-ctl
fi

echo -e "${BLUE}[5/5] Configuring Dynamic Auto-Unbind daemon (Zero-Host-Lockout) & Discovery...${NC}"
# Purge legacy unconditional autobind services & rules from older versions (prevents re-bind loops)
systemctl stop snakeusbip-autobind 2>/dev/null || true
systemctl disable snakeusbip-autobind 2>/dev/null || true
rm -f /etc/systemd/system/snakeusbip-autobind.service
rm -f /usr/local/bin/snakeusbip-autobind.sh
rm -f /etc/udev/rules.d/99-usbip-autobind.rules
rm -f /etc/udev/rules.d/99-snakeusbip-autobind.rules

# Install DualSense / DualSense Edge udev protection rule (inhibits hid-playstation race, USB autosuspend & ARM64 isoc audio Oops)
cat << 'UDEV_EOF' > /etc/udev/rules.d/99-snakeusbip-dualsense-fix.rules
# SnakeUSBIP — Prevent hid-playstation race, USB autosuspend, and ARM64 usbip_host isoc audio Oops on Sony DualSense / DualSense Edge
ACTION=="add", SUBSYSTEM=="usb", ATTR{idVendor}=="054c", ATTR{idProduct}=="0ce6", ATTR{power/control}="on"
ACTION=="add", SUBSYSTEM=="usb", ATTR{idVendor}=="054c", ATTR{idProduct}=="0df2", ATTR{power/control}="on"
ACTION=="add", SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_interface", ATTRS{idVendor}=="054c", ATTRS{idProduct}=="0ce6", ATTR{bInterfaceClass}=="01", ATTR{authorized}="0"
ACTION=="add", SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_interface", ATTRS{idVendor}=="054c", ATTRS{idProduct}=="0df2", ATTR{bInterfaceClass}=="01", ATTR{authorized}="0"
ACTION=="add", SUBSYSTEM=="hid", ATTRS{idVendor}=="054c", ATTRS{idProduct}=="0ce6", RUN+="/bin/sh -c 'echo $kernel > /sys/bus/hid/drivers/playstation/unbind 2>/dev/null || true'"
ACTION=="add", SUBSYSTEM=="hid", ATTRS{idVendor}=="054c", ATTRS{idProduct}=="0df2", RUN+="/bin/sh -c 'echo $kernel > /sys/bus/hid/drivers/playstation/unbind 2>/dev/null || true'"
UDEV_EOF

udevadm control --reload-rules 2>/dev/null || true
udevadm trigger 2>/dev/null || true
mkdir -p /etc/snakeusbip

# Install Dynamic Auto-Unbind & Control API service (now snakeusbip-ctl is guaranteed to exist!)
cat << 'EOF' > /etc/systemd/system/snakeusbip-autounbind.service
[Unit]
Description=SnakeUSBIP Dynamic Auto-Unbind & Control Daemon
After=network.target usbipd.service
Wants=usbipd.service

[Service]
Type=simple
Environment=PYTHONUNBUFFERED=1
ExecStart=/usr/bin/python3 /usr/local/bin/snakeusbip-ctl dynamic-daemon
Restart=always
RestartSec=3
KillMode=process

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload 2>/dev/null || true
systemctl enable snakeusbip-autounbind 2>/dev/null || true
systemctl restart snakeusbip-autounbind 2>/dev/null || true

# Configure Avahi Zeroconf / mDNS service
if command -v avahi-daemon &> /dev/null; then
    mkdir -p /etc/avahi/services
    cat << 'AVAHI_EOF' > /etc/avahi/services/snakeusbip.service
<?xml version="1.0" standalone="no"?>
<!DOCTYPE service-group SYSTEM "avahi-service.dtd">
<service-group>
  <name replace-wildcards="yes">SnakeUSBIP (%h)</name>
  <service>
    <type>_snakeusbip._tcp</type>
    <port>3240</port>
    <txt-record>proto=usbip</txt-record>
    <txt-record>version=1.1.1</txt-record>
  </service>
  <service>
    <type>_usbip._tcp</type>
    <port>3240</port>
  </service>
</service-group>
AVAHI_EOF
    systemctl restart avahi-daemon 2>/dev/null || true
fi

echo -e "\n${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✓ SnakeUSBIP Server & Control Suite installed successfully!        ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo -e "• Server daemon is listening on TCP port ${BOLD}3240${NC}."
echo -e "• Run ${CYAN}snakeusbip-ctl${NC} anytime to open the interactive Control Suite dashboard."
echo -e "• Run ${CYAN}snakeusbip-ctl doctor${NC} to perform a complete system health check."
echo -e "• Connect from your PC using ${CYAN}SnakeUSBIP Client${NC}!\n"
