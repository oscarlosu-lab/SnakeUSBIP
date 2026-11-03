# 🔒 Privacy Policy — SnakeUSBIP

🌐 **Language / Idioma:** **English** | [Español](PRIVACY_ES.md)

**Effective Date:** November 1, 2026  
**Project:** SnakeUSBIP (Client, Server & Android)  
**Maintainer:** Oscar Losu ([@oscarlosu-lab](https://github.com/oscarlosu-lab))  
**License:** GNU General Public License v3.0 (GPL-3.0)

[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support%20Project-FF5E5B?style=flat-square&logo=ko-fi&logoColor=white)](https://ko-fi.com/oscarlosu)

---

## 1. Core Privacy Philosophy: Zero-Telemetry & Zero-Tracking

We believe that software tools, especially low-level networking and hardware utilities, must respect user privacy by default. 

**SnakeUSBIP is built on a strict Zero-Telemetry, Zero-Tracking, and Zero-Intrusion architecture:**
* **No Telemetry**: We do not collect, monitor, log, or transmit any analytics, crash metrics, or diagnostic telemetry.
* **No Tracking SDKs**: No third-party analytical frameworks (such as Google Analytics, Firebase, Sentry, AppCenter, or Microsoft Telemetry) are integrated into any binary (Windows, macOS, Linux, or Android).
* **No User Profiling or Advertising**: We do not track your hardware identifiers, advertising IDs, or online activity.
* **No Cloud Middleman**: There are no remote relay servers or proprietary cloud endpoints operated by SnakeUSBIP. All USB traffic travels directly peer-to-peer between your client and your server.

---

## 2. Information Handled & Network Traffic

### 2.1. USB-over-IP Transmission (URBs)
* **What is transmitted:** Raw USB Request Blocks (URBs), USB descriptors, and device I/O control data necessary to emulate and operate your USB peripherals over IP.
* **Where it goes:** Data flows **strictly peer-to-peer (P2P)** across your local network (LAN) or your private VPN tunnel directly between the SnakeUSBIP Client and the SnakeUSBIP Server specified by you.
* **Encryption & Transit:** USB/IP is an open RFC-based protocol designed for low-latency network communication. When transmitting across untrusted networks or the public Internet, users should always encapsulate the traffic within an encrypted VPN tunnel (such as WireGuard, OpenVPN, or SSH tunneling, both supported natively in the Client UI).

### 2.2. Local Network Discovery (mDNS & Subnet Broadcasts)
* When you initiate a server scan via the Client application, SnakeUSBIP broadcasts discovery probes on your local subnet (UDP port 3240) or resolves standard mDNS records (`_usbip._tcp.local.`).
* These discovery packets **never leave your local area network (LAN)**.

### 2.3. Software Update Checks
* When checking for updates (either manually or via the update check setting), SnakeUSBIP sends a secure HTTPS GET request to the public GitHub API:
  `https://api.github.com/repos/oscarlosu-lab/SnakeUSBIP/releases/latest`
* Only standard anonymous HTTP headers provided by your operating system are sent to GitHub. No personal data, device identifiers, or usage statistics are attached.

---

## 3. Local Data Storage

All user configurations and persistent data are stored exclusively on your local machine:
* **Windows Desktop**: Settings and favorites are stored locally in `%APPDATA%\SnakeUSBIP\config.json` (or in the local application folder when running in Portable mode).
* **Android**: Preferences are stored strictly within the app's protected internal storage sandbox via Android DataStore / SQLite cache. Application backups are explicitly disabled (`android:allowBackup="false"`) to prevent unauthorized extraction via ADB.
* **Linux & macOS**: Stored in standard XDG configuration paths (`~/.config/snakeusbip/`).

No configuration, device aliases, or connection history are ever uploaded to any remote server.

---

## 4. Operating System Permissions

SnakeUSBIP requests only the operating system permissions strictly required for hardware mediation:
* **Windows (Administrator Privileges)**: Required solely to install and interact with the USB/IP virtual bus driver (`vhci`) via Windows SetupAPI / PnPUtil and bind network sockets on privileged ports.
* **Android (USB Host & Foreground Service)**:
  * `android.permission.FOREGROUND_SERVICE_CONNECTED_DEVICE`: Keeps the USB/IP server daemon alive while forwarding peripherals in the background.
  * `android.hardware.usb.host`: Communicates directly with OTG peripherals plugged into the USB port.
  * **Zero-Intrusion Policy**: All background startup hooks (e.g., auto-start on boot, auto-start on USB connect) are **disabled by default**. SnakeUSBIP never runs in the background without explicit user opt-in.

---

## 5. Formal Compliance Statement

In compliance with open-source code signing and software distribution governance (including SignPath Foundation and Microsoft Store security guidelines):

> **Official Privacy Statement:**  
> *This program will not transfer any information to other networked systems unless specifically requested by the user or the person installing or operating it.*

---

## 6. Open Source Transparency & Verification

The entirety of SnakeUSBIP's source code is publicly accessible under the **GNU General Public License v3.0**. Anyone can independently audit, inspect, build, and verify the network behavior and source code:
* **Source Repository**: [github.com/oscarlosu-lab/SnakeUSBIP](https://github.com/oscarlosu-lab/SnakeUSBIP)
* **Automated Security Audits**: All code is continuously audited via GitHub CodeQL (SAST) and Gitleaks secret scanning on every release.

---

## 7. Contact & Support

If you have any questions or security inquiries regarding this privacy policy:
* **GitHub Issues**: [github.com/oscarlosu-lab/SnakeUSBIP/issues](https://github.com/oscarlosu-lab/SnakeUSBIP/issues)
* **Project Maintainer**: Oscar Losu ([@oscarlosu-lab](https://github.com/oscarlosu-lab))
* **Support the Project**: [ko-fi.com/oscarlosu](https://ko-fi.com/oscarlosu)

