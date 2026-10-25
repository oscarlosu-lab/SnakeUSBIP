#!/usr/bin/env bash
# ==============================================================================
# 🌐 USBAnywhere — 1-Click Linux & Raspberry Pi Plug & Play Server Installer
# https://github.com/oscarlosu-lab/USBAnywhere
#
# Usage:
#   curl -sSL https://raw.githubusercontent.com/oscarlosu-lab/USBAnywhere/main/scripts/install-server.sh | sudo bash
#
# Features:
#   1. Installs usbip, hwdata, and usbutils across Debian/Ubuntu/PiOS/Fedora/Arch
#   2. Loads usbip_core & usbip_host kernel modules persistently across reboots
#   3. Creates a systemd service (usbanywhere-server.service) running usbipd
#   4. Sets up a udev rule + auto-bind helper so any USB device plugged into the
#      server is automatically exported to Windows (100% Plug & Play like VirtualHere!)
# ==============================================================================

set -e

echo "================================================================"
echo " 🌐 USBAnywhere Server Installer (Plug & Play Edition)"
echo "================================================================"

if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run as root (use sudo)."
    exit 1
fi

# 1. Detect Package Manager & Install Dependencies
echo "[1/4] Installing USB/IP packages..."
if command -v apt-get >/dev/null 2>&1; then
    apt-get update -qq
    # Try standard usbip package first, fallback to linux-tools-generic (Ubuntu)
    apt-get install -y usbip hwdata usbutils 2>/dev/null || \
    apt-get install -y "linux-tools-$(uname -r)" linux-tools-generic hwdata usbutils
elif command -v dnf >/dev/null 2>&1; then
    dnf install -y usbip hwdata usbutils
elif command -v pacman >/dev/null 2>&1; then
    pacman -Sy --noconfirm usbip hwdata usbutils
elif command -v opkg >/dev/null 2>&1; then
    opkg update && opkg install usbip-server kmod-usb-ohci usbutils
else
    echo "⚠️ Unsupported package manager. Ensure 'usbip' and 'usbipd' are installed."
fi

# 2. Load Kernel Modules Persistently
echo "[2/4] Enabling kernel modules (usbip_core, usbip_host)..."
modprobe usbip-core 2>/dev/null || true
modprobe usbip_host

mkdir -p /etc/modules-load.d
cat << 'EOF' > /etc/modules-load.d/usbanywhere.conf
usbip-core
usbip_host
EOF

# 3. Create Auto-Bind Helper Script (Excludes USB Hubs & Onboard Network Adapters)
echo "[3/4] Installing Plug & Play Auto-Bind script..."
cat << 'EOF' > /usr/local/bin/usbanywhere-autobind.sh
#!/usr/bin/env bash
# Auto-binds all external USB devices while safely skipping root hubs and internal NICs

USBIP_BIN=$(command -v usbip || echo "/usr/sbin/usbip")

for devpath in /sys/bus/usb/devices/*; do
    busid=$(basename "$devpath")
    # Skip interfaces (containing ':') and root usb buses ('usb1', 'usb2', etc.)
    [[ "$busid" == *:* ]] && continue
    [[ "$busid" == usb* ]] && continue
    [[ ! -f "$devpath/idVendor" ]] && continue

    bDeviceClass=$(cat "$devpath/bDeviceClass" 2>/dev/null || echo "")
    idVendor=$(cat "$devpath/idVendor" 2>/dev/null || echo "")
    idProduct=$(cat "$devpath/idProduct" 2>/dev/null || echo "")

    # Skip USB Hubs (Class 09)
    [[ "$bDeviceClass" == "09" ]] && continue

    # Skip Raspberry Pi onboard SMSC/Microchip USB Ethernet bridges
    [[ "$idVendor:$idProduct" == "0424:ec00" ]] && continue
    [[ "$idVendor:$idProduct" == "0424:7800" ]] && continue

    # Skip USB mass storage devices currently mounted as root/boot filesystem
    if ls "$devpath"/*/block/* >/dev/null 2>&1; then
        continue
    fi

    # Bind device if not already bound to usbip-host
    driver_link=$(readlink "$devpath/driver" 2>/dev/null || echo "")
    if [[ "$driver_link" != *"usbip-host"* ]]; then
        "$USBIP_BIN" bind -b "$busid" >/dev/null 2>&1 || true
    fi
done
EOF
chmod +x /usr/local/bin/usbanywhere-autobind.sh

# 4. Configure systemd service & udev hotplug rule
echo "[4/4] Configuring systemd daemon and udev hotplug rules..."
if command -v systemctl >/dev/null 2>&1; then
    USBIPD_BIN=$(command -v usbipd || echo "/usr/sbin/usbipd")
    cat << EOF > /etc/systemd/system/usbanywhere.service
[Unit]
Description=USBAnywhere USB/IP Server Daemon
After=network.target

[Service]
Type=forking
ExecStart=${USBIPD_BIN} -D
ExecStartPost=/usr/local/bin/usbanywhere-autobind.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable usbanywhere.service
    systemctl restart usbanywhere.service
else
    usbipd -D || true
    /usr/local/bin/usbanywhere-autobind.sh || true
fi

if [ -d /etc/udev/rules.d ]; then
    cat << 'EOF' > /etc/udev/rules.d/99-usbanywhere-autobind.rules
ACTION=="add", SUBSYSTEM=="usb", ENV{DEVTYPE}=="usb_device", RUN+="/usr/local/bin/usbanywhere-autobind.sh"
EOF
    udevadm control --reload-rules 2>/dev/null || true
fi

IP_ADDR=$(hostname -I 2>/dev/null | awk '{print $1}')
echo ""
echo "✅ USBAnywhere Server is active and running on port 3240!"
echo "📡 Server IP: ${IP_ADDR:-<your-server-ip>}"
echo "🔌 Plug & Play Auto-Export is ENABLED: any USB device plugged in is shared automatically."
echo "----------------------------------------------------------------"
usbip list -l 2>/dev/null || true
echo "================================================================"
