<div align="center">

# 🐍 SnakeUSBIP v3.0

**The Free, Open-Source VirtualHere Alternative for Windows, Android, macOS & Linux**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg?style=flat-square)](https://www.gnu.org/licenses/gpl-3.0)
[![.NET 9.0](https://img.shields.io/badge/.NET-9.0-purple.svg?style=flat-square&logo=dotnet)](https://dotnet.microsoft.com/)
[![Platforms](https://img.shields.io/badge/Platforms-Windows%20%7C%20Android%20%7C%20macOS%20%7C%20Linux-green.svg?style=flat-square)]()
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support%20Project-FF5E5B?style=flat-square&logo=ko-fi&logoColor=white)](https://ko-fi.com/oscarlosu)

[English](README.md) | [Español](README_ES.md)

</div>

---

## 🌐 Overview

**SnakeUSBIP** is a unified, multi-platform USB-over-IP suite designed to connect unlimited USB devices over LAN, Wi-Fi, and the Internet with ultra-low latency. It provides a complete, modern, and 100% free open-source alternative to commercial solutions like VirtualHere.

### ✨ Key Features
- **Client GUI (Windows WPF)**: Modern interface, auto-discovery (mDNS), 1-click device mounting, auto-reconnect, and multi-server management.
- **Unified Server (.NET 9 / CLI / Swift)**: High-performance USB/IP daemon supporting Windows, Linux (`snakeusbip-ctl`), and native macOS Apple Silicon.
- **Android Rootless Server**: Turn any Android phone, tablet, or Android TV device into a USB/IP server without root. Sunshine game streaming handoff with full DualSense haptics and sim racing Force Feedback (FFB).
- **Hardened Security & Integrity**: Native AOT compiled binaries, deterministic SHA-256 integrity proofs, and zero-telemetry.

---

## 📁 Monorepo Structure

```text
SnakeUSBIP/
├── client/          # Windows WPF Client GUI & tray controller
├── server/          # Multi-platform Server (.NET 9 Windows, Swift macOS, Linux CLI)
├── android/         # Android / Android TV rootless server application
├── tools/           # Build automation & hardened protection pipelines
├── docs/            # Complete technical documentation & guides
├── docker/          # Dockerized Linux USB/IP server
└── SnakeUSBIP.sln   # Visual Studio / .NET unified solution
```

---

## 🚀 Quick Start & Building

### Prerequisites
- [.NET 9.0 SDK](https://dotnet.microsoft.com/download/dotnet/9.0)
- Java 17+ & Android SDK (for Android builds)

### 1. Build Client & Server (.NET 9)
```powershell
dotnet restore SnakeUSBIP.sln
dotnet build SnakeUSBIP.sln -c Release
dotnet test SnakeUSBIP.sln -c Release
```

### 2. Build Android App
```bash
cd android
./gradlew assembleRelease
```

---

## ☕ Support the Project

SnakeUSBIP is 100% free and open-source software under the **GNU General Public License v3 (GPLv3)**. If SnakeUSBIP helps your workflow or gaming setup, consider supporting its ongoing development:

[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support%20Project-FF5E5B?style=flat-square&logo=ko-fi&logoColor=white)](https://ko-fi.com/oscarlosu)

---

## ⚖️ License & Trademark

- **License**: [GNU General Public License v3](LICENSE).
- **Trademark Notice**: SnakeUSBIP is an independent open-source project maintained by `oscarlosu-lab`.
