# 📖 SnakeUSBIP User Manual

🌐 **Language / Idioma:** **English** | [Español](USAGE_ES.md)

## Main Interface

```
╔═══════════════════════════════════════════════════════════════════╗
║ 🦊 SnakeFoxu   USB/IP Manager   [ENG] [🔄 Update]      🟡 🟢 🔴  ║
╠═══════════════════════════════════════════════════════════════════╣
║  Server:  ┌──────────────┐ ┌─────────┐┌──────┐┌─────┐┌─────────┐  ║
║           │192.168.1.100 │ │🔍 Scan  ││🔄List││🖥️SSH││🌐 VPN  │  ║
║           └──────────────┘ └─────────┘└──────┘└─────┘└─────────┘  ║
╠═══════════════════════════════════════════════════════════════════╣
║  📡 USB Hubs (3)                                                  ║
║   ├─ 🖥️ 192.168.1.100 (2)                                        ║
║   │   ├─ 📱 1-1.2: Arduino Uno (2341:0043)                        ║
║   │   └─ 🖨️ 1-1.4: HP LaserJet (03f0:002a)                       ║
║   └─ 🖥️ 192.168.1.101 (1)                                        ║
║       └─ 💾 1-1.1: SanDisk USB (0781:5567)                        ║
║                                                                   ║
║  ✅ Connected Devices (1)                                         ║
║   └─ 🔌 Port 00: Arduino Uno ← 192.168.1.100                      ║
║                                                                   ║
║  ⭐ Favorites (2)                                                 ║
║   ├─ 🖨️ 1-1.4 @ 192.168.1.100                                    ║
║   └─ 💾 1-1.1 @ 192.168.1.101                                     ║
╠═══════════════════════════════════════════════════════════════════╣
║ 📋 Activity Log                                        [Clear]    ║
╠───────────────────────────────────────────────────────────────────╣
║ [14:32:15] ✅ Connected: Arduino Uno (1-1.2) from 192.168.1.100   ║
║ [14:32:10] 🔍 Scanning network 192.168.1.0/24...                  ║
║ [14:32:12] ✅ 2 server(s) found                                   ║
║ [14:30:05] ⚠️ Timeout connecting to 192.168.1.50                  ║
╠═══════════════════════════════════════════════════════════════════╣
║  ✓ Ready         Drivers: ✅ Installed     [Install][Uninstall]  ║
╚═══════════════════════════════════════════════════════════════════╝
```

### Title Bar (macOS style)
```
┌──────────────────────────────────────────────────────────────────┐
│ 🦊 SnakeFoxu   USB/IP Manager   [🌐ENG] [🔄Update]     🟡 🟢 🔴 │
└──────────────────────────────────────────────────────────────────┘
                                                          │  │  │
                                              Minimize ───┘  │  │
                                              Maximize ──────┘  │
                                              Close ────────────┘
```

### Server Panel
```
┌──────────────────────────────────────────────────────────────────────┐
│ Server: [__192.168.1.100__] [🔍 Scan ][🔄List][🖥️SSH][🌐 VPN]       │
└──────────────────────────────────────────────────────────────────────┘
                │                    │          │        │       │
  Server IP     │    Search network ─┘          │        │       │
  (editable)    │    (scans subnet)             │        │       │
                │                               │        │       │
                │         List devices ─────────┘        │       │
                │         from current server            │       │
                │                                        │       │
                │              SSH Configuration ────────┘       │
                │              for Raspberry Pi                  │
                │                                                │
                │                     Internet Connection ───────┘
                │                     (Tailscale/ZeroTier)
```

## Main Actions

### 🔍 Scan
Searches for USB/IP servers on your local network (port 3240).

### 🔄 List
Shows available USB devices on the server.

### 🖥️ SSH
Opens configuration to connect to Raspberry Pi via SSH.

### 🌐 VPN
Connect to remote USB/IP servers over Internet using Tailscale or ZeroTier.
See [VPN_INTERNET_EN.md](VPN_INTERNET_EN.md) for complete configuration.

## Context Menu (Right Click)

```
┌─────────────────────────────────────┐
│ 📱 1-1.4: Arduino Uno              │ ← Right-click here
└─────────────────────────────────────┘
                    │
                    ▼
        ┌─────────────────────────┐
        │ 🔌 Connect              │
        │ ❌ Disconnect           │
        ├─────────────────────────┤
        │ ⭐ Add to Favorites     │
        │ ❌ Remove from Favorites│
        │ 🗑️ Remove server        │
        ├─────────────────────────┤
        │ 📋 Properties           │
        └─────────────────────────┘
```

| Option | Description |
|--------|-------------|
| 🔌 Connect | Connects the remote USB device to your PC |
| ❌ Disconnect | Releases the connected USB device |
| ⭐ Add to Favorites | Saves the device for quick reconnection |
| ❌ Remove from Favorites | Removes from favorites list |
| 🗑️ Remove server | Removes server from tree |
| 📋 Properties | Shows detailed info (VID:PID, manufacturer, etc.) |

## Shortcuts

- **Double-click** on device → Connect
- **Enter** in IP field → List devices
- **F5** → Refresh list

## Favorites & Performance Modes

Favorites are saved in `config.json` and can auto-reconnect when starting the application.

### ⚡ USB/IP Performance Modes

SnakeUSBIP supports tunable network connection profiles via `--receive-mode`:

| Mode | Best for | Technical Description |
|---|---|---|
| **Zero-Copy** *(Default)* | Storage disks, flash drives, HD webcams | Utilizes direct network buffers without intermediate kernel copies, delivering maximum throughput. |
| **Low-Latency** | Mice, keyboards, game controllers, HID | Powered by Winsock Kernel (WSK) event callbacks to minimize input lag on high-polling devices. |

### 🔌 Clean Graceful Detach

When closing the application or shutting down Windows (`AutoDetachOnExit: true`), SnakeUSBIP gracefully detaches and releases all active USB ports before terminating. This prevents the remote Linux server from leaving ports in a locked (*busy*) state, allowing immediate re-connections without needing to restart server daemons.

## 📝 Activity Log

```
╔════════════════════════════════════════════════════════════════╗
║ 📋 Activity Log                                        [Clear] ║
╠════════════════════════════════════════════════════════════════╣
║ [14:35:22] ✅ Connected: Arduino Uno (1-1.2) from 192.168.1.10 ║
║ [14:35:20] 🔍 Listing devices on 192.168.1.100...              ║
║ [14:35:15] ✅ 2 server(s) found                                ║
║ [14:35:10] 🔍 Scanning network 192.168.1.0/24...               ║
║ [14:34:55] ❌ Error: Timeout connecting to 192.168.1.50        ║
║ [14:34:50] ⚠️ Drivers not detected, installing...              ║
║ [14:34:45] ✅ Drivers verified OK                               ║
╚════════════════════════════════════════════════════════════════╝
```

The bottom panel shows a real-time event history:

| Icon | Type | Description |
|------|------|-------------|
| ✅ | Success | Successful connections, servers found, drivers OK |
| ❌ | Error | Connection failures, timeouts, unavailable devices |
| 🔍 | Info | Scans in progress, informational operations |
| ⚠️ | Warning | Minor issues, incomplete configuration |

Use the **[Clear]** button to clear the history.

## 🖥️ System Tray

```
                                    ┌─────────────────────────────┐
                                    │   System Tray               │
                                    │   (next to the clock)       │
                                    └──────────┬──────────────────┘
                                               │
     ┌─────────────────────────────────────────┼────────────────────┐
     │  🔊  📶  🔋  ⚡ ... 🦊                  │                    │
     └─────────────────────────────────────────┼────────────────────┘
                                               │
                                               ▼ Right-click
                                    ┌─────────────────────────┐
                                    │ 📡 Scan Network         │
                                    │ 🔼 Show Window          │
                                    ├─────────────────────────┤
                                    │ ❌ Exit                 │
                                    └─────────────────────────┘
```

- When **minimizing**, the app hides to the system tray (🦊 icon)
- **Double-click** on the icon to restore the window
- **Right-click** for quick menu: Scan Network, Show Window, Exit
- The app keeps running in the background until you press "Exit"

## 🌐 Change Language

```
┌──────────────────────────────────────────────────────────────────┐
│ 🦊 SnakeFoxu   USB/IP Manager   [🌐ENG] [🔄Update]     🟡 🟢 🔴 │
└──────────────────────────────────────────────────────────────────┘
                                      │
                            Click here│
                                      ▼
                            ┌────────────────┐
                            │ 🌐 ENG → ESP   │  (toggles)
                            │ 🌐 ESP → ENG   │
                            └────────────────┘
```

Use the **[🌐 ENG]** or **[🌐 ESP]** button in the title bar to toggle between English and Spanish. The language is automatically saved in `config.json`.

## 🔧 Status Bar and Drivers

```
╔════════════════════════════════════════════════════════════════════╗
║  ✓ Ready         Drivers: ✅ Installed       [Install][Uninstall] ║
╚════════════════════════════════════════════════════════════════════╝
     │                   │                          │          │
     │                   │               Install ───┘          │
     │                   │               USB/IP drivers        │
     │                   │                                     │
     │                   │                    Uninstall ───────┘
     │                   │                    (requires restart)
     │                   │
     Current status ─────┘                   
     of the connection   Driver status ──────┘
                         ✅ Installed
                         ❌ Not installed
```

> ⚠️ **Important:** The first driver installation may require restarting Windows.

---

## 🆘 Troubleshooting

### "No server found"
1. Verify the USB/IP server is running: `sudo usbipd` on Linux
2. Check that port 3240 is open in the firewall
3. Verify you're on the same subnet (e.g., 192.168.1.x)

### "Error connecting device"
1. Make sure drivers are installed (bottom bar)
2. The device must be "bound" on the server: `sudo usbip bind -b X-X`
3. Run SnakeUSBIP as Administrator

### "Device connected but not working"
1. Check Device Manager if it needs additional drivers
2. Some USB 3.0 devices may not be compatible
3. Try another USB port on the server

---

## 📚 More Information

- **[README.md](../README.md)** - Installation and features
- **[RASPBERRY_PI_SERVER_EN.md](RASPBERRY_PI_SERVER_EN.md)** - Configure server on Raspberry Pi
- **[CHANGELOG.md](../CHANGELOG.md)** - Version history
