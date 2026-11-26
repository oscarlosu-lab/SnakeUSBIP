# ⚡ SnakeUSBIP Automation & Setup Scripts

🌐 **Language / Idioma:** **English** | [Español](README_ES.md)

This directory contains provisioning scripts, control suites, and media automation tools for the SnakeUSBIP ecosystem.

[![License](https://img.shields.io/badge/License-GPLv3-blue.svg?style=flat-square)](https://www.gnu.org/licenses/gpl-3.0)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support%20Project-FF5E5B?style=flat-square&logo=ko-fi&logoColor=white)](https://ko-fi.com/oscarlosu)

---

## 📜 Script Index

### 1. `snakeusbip-ctl` — Unified Control Suite (macOS & Linux)
Interactive Terminal User Interface (TUI) dashboard and CLI management tool with zero external dependencies.
- **Interactive TUI Dashboard**: `snakeusbip-ctl` (or `snakeusbip-ctl dashboard`)
- **Dashboard Mode**: `snakeusbip-ctl mode [server|client|both]` (asked on first launch; switch anytime with `[m]`)
- **Optional Client Sleep Guard (Linux client)**: disabled by default. Installing the script, opening the dashboard and connecting devices do not install or enable any service. From the dashboard (`[g]`), you can choose **Disabled**, **Temporary** (active only while the dashboard is open, stops on exit), or **Permanent** (background systemd service, starts at boot). From the CLI: `sudo snakeusbip-ctl client-guard install|uninstall|status`. Ordinary connect/disconnect works without it. When active, it listens for logind `PrepareForSleep`, holds a sleep delay inhibitor, detaches imported USB/IP devices before suspend (verified in vhci_hcd sysfs) and re-attaches them on resume once the server answers on TCP 3240. Logs: `journalctl -u snakeusbip-client-guard`. Requires Linux with systemd/logind, `busctl`, `systemd-inhibit`, `udevadm` and `usbip`. Lid behavior is not configured by SnakeUSBIP.
- **System Doctor**: `snakeusbip-ctl doctor`
- **Protocol Loopback Test**: `snakeusbip-ctl test`
- **Service Control**: `sudo snakeusbip-ctl start|stop|restart|status`
- **Device Management**: `snakeusbip-ctl list`, `sudo snakeusbip-ctl share <busid>`
- **Linux Client Mode (`vhci_hcd`)**: `snakeusbip-ctl scan|remote <ip>`, `sudo snakeusbip-ctl connect|disconnect|ports`
- **Security Policy (`TCP 3241`)**: `sudo snakeusbip-ctl policy show|allow|deny|protect-hid|allow-ip|deny-ip|set-token|clear-token`
- **DualSense SBC Fix**: `sudo snakeusbip-ctl fix-dualsense enable|disable|status`

### 2. `install-server-mac.sh` — 1-Click macOS Server Installer
Automated installer for macOS (Apple Silicon M1-M4 & Intel x86_64).
- Installs native Swift server daemon and LaunchDaemon service.
- Installs `snakeusbip-ctl` to `/usr/local/bin/`.

```bash
curl -fsSL https://raw.githubusercontent.com/oscarlosu-lab/SnakeUSBIP/main/server/scripts/install-server-mac.sh | sudo bash
```

### 3. `install-server-linux.sh` / `install-server.sh` — 1-Click Linux / Raspberry Pi Installer
Automated installer for Linux distributions and Raspberry Pi OS (Debian/Ubuntu/Raspbian/Arch/Fedora).
- Automatically loads `usbip_core` and `usbip_host` kernel modules.
- Installs `usbip` userspace package and systemd daemon.
- Configures udev hotplug auto-exporting rule.
- Installs `snakeusbip-ctl` to `/usr/local/bin/`.

```bash
curl -fsSL https://raw.githubusercontent.com/oscarlosu-lab/SnakeUSBIP/main/server/scripts/install-server-linux.sh | sudo bash
```

---

## 📄 License

GPL-3.0 License. Developed by [oscarlosu-lab](https://github.com/oscarlosu-lab).
