# CHANGELOG - SnakeUSBIP

## [1.4.1] - 2026-11-28

> **Migration Notice:** `SnakeUSBIP` is being migrated into [USBAnywhere](https://github.com/oscarlosu-lab/USBAnywhere). `SnakeUSBIP` acts as the staging branch for new improvements prior to full stabilization, while `USBAnywhere` is the final production product.

### Fixed
- **Windows Client `MainWindow` Layout & ES/EN Localization (`MainWindow.xaml`, `MainWindow.xaml.cs`, `LocalizationService.cs`)**:
  - Expanded window dimensions to `780x820` (`MinWidth=760`, `MinHeight=780`), converted the title bar to a 3-column responsive grid, widened the server IP box/toolbar buttons, and separated bottom status-bar checkboxes (`chkSessionIsolation` on its own row) from `btnReceiveMode` / driver buttons to eliminate overlapping controls.
  - Added full ES/EN localization for `btnPair`, `chkLocalApi`, `btnCopyApiToken`, `chkSessionIsolation`, and the `menuAttachMode` context submenu.
- **GitHub Pages & Documentation Parity (`docs/index.html`, `docs/*.md`, `SECURITY*.md`)**:
  - Updated GitHub Pages, refreshed `capture_01_mainwindow_dark.png`, and updated all user/security manuals for `v1.4.0`/`v1.4.1`.

## [1.4.0] - 2026-11-27

> **Migration Notice:** `SnakeUSBIP` is being migrated into [USBAnywhere](https://github.com/oscarlosu-lab/USBAnywhere). `SnakeUSBIP` acts as the staging branch for new improvements prior to full stabilization, while `USBAnywhere` is the final production product.

### Added
- **Zero-Config 6-Digit / `UA2:` Pairing & Pinned TLS 1.3 Tunnel (`PairingService`, `TlsTunnelService`, `PairServerDialog`, `TlsTunnelBridge`)**:
  - End-to-end 6-digit pairing codes, `UA2:` QR/tokens, SHA-256 certificate pinning, automatic client TLS loopback bridging in `UsbipService`, and `BindAddress` scoping across Windows Client/Server, Linux (`snakeusbip-ctl`), and Android.
- **Multi-Provider Streaming Handoff, Multi-Session Isolation & Automation (`StreamingSessionMonitor`, `SessionIsolationService`, `LocalControlApiService`, `snakeusbip-mcp.py`)**:
  - Added support for **Sunshine, Apollo, Vibeshine, Vibepollo, Parsec, and Steam Remote Play**, `only-during-stream` device modes, WTS session isolation, loopback REST API (`127.0.0.1:13241`), 6-tool stdio MCP server, and `docs/HOME_ASSISTANT.md`.
- **Smart Favorites `[Rev:XXXX]` Disambiguation, Driver `0.9.8.2` Dual-ABI & macOS `IOUSBHost` (`SnakeUSBIP.Server.Mac`)**:
  - Added hardware revision disambiguation + Server `Rev` column, `IOUSBHost` & `AVAudioEngine` virtual microphone support on macOS, Linux automatic USB autosuspend disablement + systemd `usbipd` drop-ins, and 8-frame square high-DPI `.ico` bundles (`16..256 px`).

### Fixed
- **Pre-Release E2E & Stress Hardening (`App.xaml.cs`, `LocalControlApiService`, `UsbipService`, `TlsTunnelService`, `DiscoveryResponderService`, `snakeusbip-ctl`, `snakeusbip-mcp.py`, Android)**:
  - Enabled non-elevated headless `--status --json` / `--doctor --json` execution with pure JSON output, `SemaphoreSlim` concurrency bounds, 5s/10s socket & TLS timeouts, HTTP `400` on malformed JSON, `TOKEN` control header propagation, and bounded `ST_NODEV` attach retries.
  - Restricted remote `PAIR_CREATE` on Linux TCP `3241` to loopback unless `control_token` is set, persisted pairing state (`0o600`), raised `listen(64)`, added non-blocking `logs` defaults, and isolated MCP `stdout`.
  - Added strict Android `busId` validation (`^\d+-[\d.]+$`), pairing payload aliases, and off-main-thread UI/QR initialization.

## [1.3.0] - 2026-11-26

> **Migration Notice:** `SnakeUSBIP` is being migrated into [USBAnywhere](https://github.com/oscarlosu-lab/USBAnywhere). `SnakeUSBIP` acts as the staging branch for new improvements prior to full stabilization, while `USBAnywhere` is the final production product.

### Added
- **Windows Kernel Boot Persistence & Custom USB Serials (`VhciNativeClient.cs`, `KernelConfigService.cs`)**:
  - Added native VHCI IOCTL support for kernel-level persistent device attachments across reboots (`SetKernelPersistentDevicesAsync`, `GetKernelPersistentDevicesAsync`), custom per-device USB serial strings, and configurable Virtual Hub USB 2.0 / USB 3.0 port counts.
- **One-Click Diagnostics Bundle Export (`KernelDiagnosticsService.cs`)**:
  - Exports a ZIP diagnostics archive containing driver state, imported VHCI ports, hub configuration, and recent logs.
- **Control Plane Hardening & UAS Storage Detection (`snakeusbip-ctl`, `ControlServer.swift`, `USBIPServer.swift`)**:
  - Added optional IP allowlist (`allowed_ips`) and constant-time HMAC `control_token` authentication (`policy allow-ip|deny-ip|set-token|clear-token`), plus UAS (`usb-storage` / `uas`) detection warnings for external SSDs.
- **Android Sunshine Webhook Token Auth & Dynamic Inventory Parser (`SunshineHandoffServer.kt`)**:
  - Added optional webhook bearer/`X-USBAnywhere-Token` authentication, HTTP header size bounds, and structured JSON inventory parsing.
- **Linux `snakeusbip-ctl` Interactive `sudo`, Dashboard Modes & Client Sleep Guard (PR #10 by @50P15)**:
  - Preserves `sudo` re-exec properly, adds `client-guard` sleep inhibitor, and adds native Linux unit tests.

### Fixed
- **Wi-Fi Dynamic Bind Resilience, `0xE102xxxx` Error Mapping & Localization (`UsbipService.cs`, `VhciNativeClient.cs`, `MainWindow.xaml.cs`)**:
  - Added retry recovery for transient `ST_NA` / `ST_DEV_BUSY` / `ST_NODEV` attach responses, human-readable `0xE102xxxx` error mapping, CLI custom serial forwarding, and ES/EN menu localization.

## [1.2.0] - 2026-11-15

### Added
- **Direct Native Windows VHCI IOCTL Client & Push Events (`VhciNativeClient.cs`)**:
  - Eliminated repeated `usbip.exe` subprocess spawning, stdout regex parsing, and per-call directory SHA-256 hashing on Windows by communicating directly with `usbip2_ude` (`GUID_DEVINTERFACE_USBIP_VHCI`) via P/Invoke `DeviceIoControl` (`GET_IMPORTED_DEVICES`, `PLUGIN_HARDWARE`, `PLUGIN_HARDWARE_ONCE`, `PLUGOUT_HARDWARE`, `STOP_ATTACH_ATTEMPTS`) with automatic multi-revision VHCI ABI compatibility and clean `usbip.exe` fallback when the kernel interface is absent.
  - Added asynchronous overlapped `ReadFile` / `CancelIoEx` push event monitoring (`RunDeviceStateListenerAsync`) to update connected device trees immediately on plug/unplug transitions.
- **Global Emergency Hotkey, Headless CLI & Tray Disconnect All (Issue #10)**:
  - Added configurable global hotkey (default `Ctrl+Alt+D`), Tray `Disconnect All`, and headless single-instance CLI commands (`--disconnect-all`, `--disconnect <port>`, `--quit`).
  - Fixed offline favorites monitor (`initiallyConnected = false`) and added background reconnect telemetry.

### Fixed
- **Windows 11 24H2/25H2 Multi-Size Tray Icon Sizing**:
  - Updated both Client and Windows Server `NotifyIcon` loaders to resolve icons at `SystemInformation.SmallIconSize` instead of a fixed `32x32` resource size, preventing blank tray slots on Windows 11.
- **Linux `usbip-host` Control IN `URB_SHORT_NOT_OK` Rejection**:
  - Added `server/patches/rpi-dwc-usbip-host/04-clear-short-not-ok.patch` restricting `URB_SHORT_NOT_OK` in `masking_bogus_flags()` to Bulk and Interrupt IN endpoints so Control IN variable-length transfers (HID feature reports, FIDO/security keys) do not fail with `-EREMOTEIO`.
- **Android String Descriptor Fallback & `bInterval == 0` Sanitizer**:
  - Added `0x03` (`USB_DT_STRING`) synthesis in `UrbSession.extractDescriptorFallback` and `sanitizeConfigDescriptor()` clamping `bInterval == 0` -> `1` on Interrupt/Isochronous endpoints for Windows `USBHUB3.sys` compatibility.

## [1.1.1] - 2026-11-11

### Fixed
- **Client Instant TCP `UNBIND` & Replug Backoff (Issue #9)**:
  - `UsbipService.DetachDeviceAsync` now dispatches an asynchronous fire-and-forget `UNBIND <busid>` to TCP `3241` alongside `usbipw detach` so Linux servers release shared devices immediately instead of waiting for the kernel status transition.
  - `ConnectionMonitorService` tracks progressive reconnect delays (`3s`, `6s`, `12s`, capped at `30s`) while `BindRemoteDeviceAsync` is retried cleanly during slow USB re-enumeration.
- **Linux Server `snakeusbip-ctl` Bind/Unbind Race & `SDEV_ST_ERROR` Recovery (Issue #9)**:
  - Added per-`busid` `threading.Lock`, `udevadm settle`, and real `/sys/bus/usb/drivers/usbip-host/<busid>/usbip_status` verification in `share_device()`.
  - Waits for `SDEV_ST_USED` (`2`) / `SDEV_ST_ERROR` (`3`) settlement and automatically unbinds/retries stalled `SDEV_ST_ERROR` devices, fixing re-attach failures after USBIP detach.
- **Raspberry Pi `dwc_otg` Kernel Patch (`usbip-host` Isochronous/DMA Fix, Issue #9)**:
  - Added `server/patches/rpi-dwc-usbip-host/` (`usbip-host-dwc-otg-dma-contig.patch`, `build-patched-usbip-host.sh`, `SHA256SUMS.txt`, and guide) eliminating `-EILSEQ` (`-71`) / kernel panics on Raspberry Pi `dwc_otg` hosts and fixed `usbip-host-y` Kbuild objects (`stub_dev.o stub_main.o stub_rx.o stub_tx.o`, omitting `usbip_common.o`).
  - Updated Release packaging so `SnakeUSBIP-Server-Linux-v*.tar.gz` bundles `patches/` out of the box.

## [1.1.0] - 2026-11-10

### Added
- **Universal Linux Client Mode (`snakeusbip-ctl` v1.1.0)**:
  - Full client support on Linux (Ubuntu, Debian, Mint, Arch, Fedora, SteamOS, Bazzite) via the kernel `vhci_hcd` virtual host controller.
  - Seamless compatibility with **On-Demand Dynamic Binding (`TCP 3241`)**: `snakeusbip-ctl` automatically queries `LIST` on TCP 3241, dispatches `BIND <busid>` prior to `usbip attach`, and sends `UNBIND <busid>` on `disconnect` to return the peripheral to the remote host.
  - New CLI commands (`scan [subnet]`, `remote <ip>`, `connect <ip> <busid>`, `disconnect [port|all]`, `ports`) and interactive Control Dashboard options (`[9]` Connect Remote Device, `[0]` Disconnect Client Port).
- **Android TV / Nvidia Shield D-Pad & Gamepad Navigation (`TvFocus.kt`)**:
  - Full remote control and gamepad navigation across all tabs, top bar actions, switches, buttons, and device cards with high-contrast focus borders (`#D2F800`) and subtle scaling (`1.02x`).

### Fixed
- **Android USB Keyboard & Pure HID Enumeration (`UrbSession.kt`, `UsbHostManager.kt`)**:
  - Fixed `USB\VID_0000&PID_0002` enumeration failure on Windows UDE clients when attaching USB keyboards and composite HID devices exported from Android (Issue #8):
    - Accurate USB speed deduction (`USB_SPEED_LOW` / `USB_SPEED_FULL` / `USB_SPEED_HIGH`) instead of hardcoding `USB_SPEED_HIGH`.
    - Cleared `URB_SHORT_NOT_OK` (`0x0001`) on USBDEVFS Bulk/Interrupt IN URBs to prevent short-packet stalls on `usbip2_ude.sys`.
    - Skipped `0x0600` (`DEVICE_QUALIFIER`) control probes on pure HID devices in `UsbHostManager.refineDevice`.
    - Added `extractDescriptorFallback` serving cached `0x01` (Device), `0x02` (Configuration), and `0x21` (HID) descriptors from `UsbDeviceConnection.getRawDescriptors()`, plus synthesized `0x22` HID Report Descriptors (Boot Keyboard, Boot Mouse, Gamepad) and benign `USBIP_STATUS_OK` completion for stalled `SET_IDLE` / `SET_PROTOCOL` requests.
- **DualSense Audio Interface De-Authorization & Raspberry Pi `dwc_otg` Diagnostics (Issue #6)**:
  - Updated `99-snakeusbip-dualsense-fix.rules` to match `ENV{DEVTYPE}=="usb_interface"` using parent `ATTRS{idVendor}=="054c"` and `ATTR{bInterfaceClass}=="01", ATTR{authorized}="0"` for both `0ce6` (DualSense) and `0df2` (DualSense Edge), plus automatic `dwc_otg` warning in `snakeusbip-ctl doctor`.
- **Unix LF Line-Ending Enforcement**:
  - Added `.gitattributes` enforcing `eol=lf` across all shell scripts (`*.sh`), `udev` rules (`*.rules`), `snakeusbip-ctl`, and `gradlew`.

---

## [1.0.1] - 2026-11-01

### Added
- **Multiplatform CI/CD Automation ($0 FOSS)**:
  - CodeQL SAST security pipeline inspecting C# (.NET 9) and Android (Java/Kotlin).
  - Automated Secret Scanning (Gitleaks) on pull requests and commits.
  - Dependabot automated weekly security updates for NuGet, Gradle, and GitHub Actions.
  - ShellCheck validation for Linux & macOS shell scripts.
  - Code hygiene and formatting gates via dotnet format.
- **Packaging Parity**:
  - Inno Setup dynamic version override via #ifndef MyAppVersion guards.
  - Verified portable win-x64, macOS Apple Silicon/Intel tarball, Linux systemd tarball, and Android APK assets.

### Fixed
- **Inno Setup Version Stamp**:
  - Fixed Windows installer compilation to respect dynamic /DMyAppVersion parameter in GitHub Actions.
- **Node.js 24 Runner Compatibility**:
  - Upgraded Java setup actions to actions/setup-java@v5 eliminating deprecation warnings.

---

## [1.0.0] - 2026-11-01

### Security & Hardening (Zero-Trust Audit Remediation)
- **Zero-Trust Remediation Across 55 Vectors**:
  - Socket isolation enforcing ExclusiveAddressUse = true and 127.0.0.1 binding on Android ADB / Serial bridges.
  - Memory bounds and DoS buffer protection restricting incoming network packets to 1 MB limits.
  - Command execution sanitization replacing arbitrary cmd.exe /c invocations with explicit arguments.
  - Native binary integrity verification ensuring fail-closed execution on tampered drivers or helper executables.
  - Whitelist fail-closed access control on dynamic server endpoints.
- **Unified Ecosystem Architecture**:
  - Consolidated Client (WPF .NET 9), Server (.NET 9), Mac Server (Swift), Linux scripts, and Android Server App into a single mono-repository SnakeUSBIP.
  - Standardized versioning across all platforms to 1.0.0 / 1.0.1.

---

## [3.2.0] - 2026-11-01

### Added
- **Obsidian Precision Design System (v3.2.0)**:
  - Complete visual overhaul across `MainWindow`, `SshDialog`, and `VpnDialog` featuring high-contrast dark obsidian surfaces (`#0B0C0E` / `#121418`), electric lime primary actions (`#D2F800` with `#0B0C0E` text), and dynamic theme switching (`DynamicResource` tokens for Dark and Light modes).
- **On-Demand Dynamic Control API & Zero-Config Discovery (TCP/UDP 3241)**:
  - Full client support for querying remote servers running in On-Demand mode (0 pre-exported devices on TCP 3240) via TCP 3241 `LIST`.
  - Synchronous response validation for TCP 3241 `BIND <busid>` (`OK` vs `DENIED` host policy feedback) with automatic post-bind stabilization retry on `usbip attach`.
  - Parallel UDP 3241 broadcast discovery (`SNAKEUSBIP_DISCOVERY_PROBE`) alongside TCP 3240 and TCP 3241 scanning in `NetworkScanner`.
- **Host Export Policy & Composite Interface Protection (`snakeusbip-ctl` v3.2.0)**:
  - Added `/etc/snakeusbip/policy.json` and `snakeusbip-ctl policy` CLI (`mode`, `allow`, `deny`, `protect-hid`, `protect-storage`, `reset`) across Linux and macOS servers.
  - Added child interface class inspection (`bInterfaceClass` for composite USB devices `0x00`/`0xef`/`0xff`), Valve Steam Controller (`28de:*`) recognition, and USB Hub (`0x09` / `1d6b:*`) exclusion.

### Fixed
- **Fixed On-Demand Dynamic Inventory Early Return**:
  - Removed premature return in `UsbipService.ListRemoteDevicesAsync` when `usbip.exe -l` returned empty stdout, allowing `TryQueryDynamicInventoryAsync` (TCP 3241) to enumerate physical devices on On-Demand servers.
- **Fixed Theme Startup Override & Button Contrast**:
  - Updated `MainWindow.ApplyTheme` to use Obsidian Precision v3.2.0 palettes instead of legacy colors, fixing unreadable text contrast on `Scan` and primary action buttons in both Dark and Light themes.
- **FixedCRLF Line Endings & Legacy Autobind Service on Linux**:
  - Enforced `eol=lf` via `.gitattributes` and added defense-in-depth CRLF stripping in `SshProvisioningService` before executing `/tmp/snakeusbip-install.sh`.
  - Updated Linux installer to stop and purge legacy `snakeusbip-autobind.service` units so `snakeusbip-autounbind.service` never re-binds released devices.
- **Fixed Auto-Reconnect Race on Manual Disconnect**:
  - Unregistered devices from `ConnectionMonitorService` prior to invoking `DisconnectAsync` to prevent background reconnect timers from firing during manual detachment.

---

## [3.1.0] - 2026-10-31

### Added
- **Start Minimized to System Tray (Issue #2)**:
  - Added unattended background startup support via `--minimized` (`-m`) CLI switch.
  - New `StartMinimized` option in configuration, interactive checkbox in the Status UI panel, and quick toggle directly in the System Tray context menu.
  - Seamless background auto-connection of favorite devices on system boot without stealing window focus.
- **Dynamic Multi-Tenant Engine & On-Demand Binding (TCP 3241)**:
  - Integrated dynamic device inventory discovery and on-demand `BIND` dispatch before `usbip attach` in `UsbipService.cs`.
  - Enables full visibility of physical USB devices on Linux hosts even when unbound from the kernel driver.
- **VR & High-Bandwidth Device Optimization Guides**:
  - Comprehensive hardware and streaming configuration documentation (`VR_FACIAL_TRACKER_GUIDE_ES.md` and `VR_FACIAL_TRACKER_GUIDE_EN.md`) covering HTC Vive Facial Tracker, Meta Quest, VRChat / VRCFaceTracking, zero-copy buffer sizing, and dedicated Wi-Fi 6E/LAN topologies.
- **Linux Server Improvements (`snakeusbip-ctl`)**:
  - Built-in sysfs status watcher automatically unbinding peripherals back to the local host when the remote client disconnects (fixes Steam Controller Lizard Mode and input hijacking).
  - New `dynamic-daemon` running on TCP 3241 for on-demand listing and binding.
  - Dedicated `snakeusbip-autounbind.service` systemd service unit.

---

## [3.0.1] - 2026-10-26

### Security & Hardening (Zero-Trust Audit)
- **Binary & DLL Integrity Gate (Findings C-01, F-04, A-02)**:
  - Synchronized and cryptographically verified SHA-256 hashes in `UsbipService` and `UsbipBinaryIntegrityTests` for `usbipw.exe`, `devnode.exe`, companion DLLs (`libusbip.dll`, `resources.dll`), and drivers across x64 and ARM64.
  - Implemented fail-closed execution gate blocking tampered or unverified native binaries and companion DLLs before launching sub-processes.
  - Mitigated binary planting vectors (F-01, F-05) by binding `pnputil.exe`, `cmd.exe`, and `wt.exe` strictly to absolute System32 and WindowsApps paths.
- **Linux & Container Security Hardening (Findings C-01, A-03, M-01, M-03)**:
  - Hardened `scripts/install-server.sh` with strict bash modes (`set -euo pipefail`), `curl -fsSL`, and a safe auto-export policy excluding local HID (Class 03: keyboards/mice) and Mass Storage (Class 08: USB disks) by default via `/etc/default/snakeusbip`.
  - Added root `.dockerignore` excluding 1.9 GB build caches, Git history, and `.env*` secrets from Docker daemon context.
  - Fixed Dockerfile context to copy `scripts/install-server.sh` and added `docker/entrypoint.sh` enforcing the safe class policy in containers.
- **Server Windows Hardening (Findings SW-01, SW-02)**:
  - Restricted Windows Firewall rules for TCP port 3240 to `profile=private,domain` and `remoteip=localsubnet` or explicit subnet whitelists.
  - Removed unused PIN configuration placeholder and bumped `Microsoft.NET.Test.Sdk` 17.12.0 for .NET 9 alignment.

### Fixed & Improved
- **Process & Lifecycle Robustness (Findings F-13, F-14, H-11, C-03)**:
  - Added recursive process tree termination (`Kill(entireProcessTree: true)`) on timeouts to eliminate orphaned USB/IP child handles.
  - Implemented non-blocking asynchronous driver status queries in `DriverService` eliminating UI startup freezes.
  - Exact `(ServerIP, BusId)` matching during device disconnect to prevent ambiguous port detachments across identical IP subnets.
  - Asynchronous graceful shutdown hooked into `OnClosing` and update flows, ensuring all active remote ports are cleanly detached.
- **UX & Observability Enhancements (Findings F-11, H-06, H-07, H-14)**:
  - Added Enter key shortcut on Server IP input field to trigger immediate server device enumeration.
  - Integrated `FileLoggerProvider` connecting standard `ILogger` to rolling daily disk logs in `%LOCALAPPDATA%\SnakeUSBIP\logs`.
  - Global unhandled exception handlers catching UI dispatcher, AppDomain, and unobserved task exceptions.
  - Explicit error reporting when checking for updates instead of ambiguous "You have the latest version".
- **Documentation & Packaging Parity (Findings F-18, B-06, M-09, M-10, M-11, C-02)**:
  - Added `README_ARM64.md` documenting Test Signing (`bcdedit /set testsigning on`) requirements on Windows ARM64.
  - Fixed 404 links and unified service names across English and Spanish documentation.
  - Updated Scoop and WinGet manifests with v3.0.1 release URLs and SHA-256 hashes.
  - Unified solution-wide versioning via `Directory.Build.props` (v3.0.1).

## [3.0.0] - 2026-10-24

### Added
- **Major Brand Evolution: SnakeUSBIP v3.0.0** 🌐
  - Rebranded from `SnakeUSBIP` to **`SnakeUSBIP`** — the free, open-source alternative to VirtualHere, VirtualUSB, and USB Network Gate.
  - Updated executable (`SnakeUSBIP.exe`), installer (`SnakeUSBIP_Setup_v3.0.0.exe`), portable packages (`x64` & `arm64`), UI header, system tray, and logs (`snakeusbip_YYYYMMDD.log`).
  - Automatic configuration migration from `%AppData%\SnakeUSBIP\config.json` to `%AppData%\SnakeUSBIP\config.json` on first startup.
- **1-Click Linux & Raspberry Pi Plug & Play Server Auto-Setup** ⚡
  - Added `⚡ 1-Click Auto-Setup` inside the SSH dialog and `scripts/install-server.sh` (`curl -sSL ... | sudo bash`) to automatically install `usbipd`, enable `usbip_core`/`usbip_host` kernel modules across reboots, configure `snakeusbip.service` (`systemd`), and install a `udev` hotplug rule (`99-snakeusbip-autobind.rules`) that auto-exports any plugged-in USB device.
- **Interactive Receive Mode Selector in Status Bar** 🏎️
  - Added live status bar toggle button (`⚡ Mode: Zero-Copy` / `🏎️ Mode: Low-Latency`) to switch kernel WSK receive modes on the fly and persist the preference in `config.json`.
- **Live Server Latency Meter (`[ms]`) & Custom Device Renaming (`✏️`)** 📊
  - Displays real-time TCP latency in milliseconds next to every discovered server in the `USB Hubs` tree.
  - Added `✏️ Rename` in the device context menu to assign custom friendly names per `VID:PID`.
- **Moonlight / Sunshine CLI Automation & Docker Server Support** 🎮
  - Added CLI flags `--minimized --connect <IP> <BUSID>` for seamless game-streaming automation.
  - Added `docker/docker-compose.yml` for deploying a Plug & Play USB/IP server on HomeLab/NAS systems (Proxmox, Unraid, TrueNAS, Synology).
- **Live VPN Peer Discovery (`Tailscale`, `ZeroTier`, `WireGuard`)** 🛡️
  - `VpnDialog` now performs live peer discovery and asynchronous TCP port `3240` probing (`1000 ms` timeout), importing selected peers directly into the main server tree.
- **Full HD 1080p Bilingual Video Tutorials (YouTube Edition)** 🎬
  - Included native 1080p MP4 video tutorials (`docs/youtube_tutorial_es.mp4` & `docs/youtube_tutorial_en.mp4`) with real WPF UI captures, neural voiceover, and `.srt` subtitles.
- **Expanded Zero-Trust Unit Test Suite (67 Tests)** 🧪
  - Expanded xUnit test suite to **67 passing tests** covering `UsbIdsService` hex normalization, custom device names, `LocalizationService` ES/EN parity, `InputValidator`, and atomic `ConfigService` persistence.

### Fixed & Hardened
- **Hardened Inno Setup Installer & Uninstaller (`SnakeUSBIP.iss`)** 📦
  - Added `AppMutex=SnakeUSBIP_SingleInstance_Mutex`, `CloseApplications=yes`, `UninstallDisplayIcon`, `--minimized` Windows startup argument, pre-install UDE node cleanup to prevent duplicate host controllers, synchronous `waituntilterminated` UDE cleanup on uninstall, and `[UninstallDelete]` cleanup of runtime directories (`logs`, `temp`, `data`).
- **Safe PnP Driver Lifecycle (`DriverService` & `CleanDrivers.ps1`)** 🛡️
  - Automatic detachment of active USB/IP devices prior to driver uninstallation.
  - Safe two-stage PnP driver removal (`/uninstall` followed by DriverStore `/force` fallback) that preserves physical USB 3.0 Root Hubs (`USB\ROOT_HUB30`) and third-party virtual USB adapters (e.g., `Parsec Virtual USB Adapter`).
  - Parallel `stdout`/`stderr` reading with 60-second process timeout in `DriverService.RunProcessAsync`.
- **USB Vendor/Product Hex Normalization (`UsbIdsService`)** 🔍
  - Fixed bug where `TrimStart('0', 'x')` stripped leading zeros from 4-digit hex VID/PIDs (`046d` Logitech, `0bda` Realtek, `045e` Microsoft, `05ac` Apple), and added automatic loading of the bundled 25,000+ entry `usb.ids` database.
- **Cryptographic Auto-Updater (`UpdateService`)** 🔄
  - Fixed `MainWindow` passing `updateInfo.HashUrl` (`SHA256SUMS.txt`) into `StartUpdateAsync` so mandatory SHA-256 verification succeeds.
- **Multi-Device Disconnect & Auto-Reconnect (`MainWindow` & `ConnectionMonitorService`)** 🔌
  - Fixed `DisconnectDeviceCoreAsync` matching `(ServerIP, BusId)` before `ServerIP` when multiple devices are attached from the same server.
  - Fixed `ConnectionMonitorService` executing all 3 reconnect attempts and firing `ConnectionRestored`.
  - Fixed `App.xaml.cs` tracking `_ownsMutex` before releasing the single-instance mutex on exit, and converted theme brushes to `DynamicResource` for live Dark/Light switching.

## [2.0.4] - 2026-10-19

### Added
- **Receive Mode Selection** ⚡
  - Added support for `--receive-mode=zero-copy` (high-throughput storage/webcams) and `--receive-mode=low-latency` (fast WSK event callbacks for HID devices like mice/keyboards).
  - Configurable via `DefaultReceiveMode` and per-favorite device settings.
- **Graceful Detach on Exit** 🔌
  - Application automatically releases all connected remote USB ports upon closing or system shutdown (`AutoDetachOnExit`), preventing the Linux server bus from remaining in a locked/busy state.
- **UDE Virtual Node Creator Integration** 🛠️
  - Integrated `devnode.exe` with SHA-256 integrity validation (`5B9C...6806`) for instantiating the `ROOT\USBIP_WIN2\UDE` virtual host controller in Windows PnP.
- **Active Device Detection** 🔍
  - Real-time PnP device queries via `pnputil /enum-devices /class USB` verifying active controller state rather than just staged DriverStore packages.
- **Unit Test Suite** 🧪
  - Added unit test coverage for `ConfigService` (atomic saving, corruption recovery, settings persistence). 49/49 tests passing.

### Fixed
- **Visual Driver Status False Positive** 🐛
  - Fixed bug in `MainWindow.xaml.cs` where missing drivers returning `"FALTANTE"` evaluated to true and displayed "Installed ✓". Now strictly checks for `"INSTALADO"`.
- **Connection Monitor Timer Re-entrancy** ⏱️
  - Fixed race conditions in `ConnectionMonitorService` by disabling `AutoReset` and ensuring sequential ticks with thread synchronization.
- **Atomic Configuration Persistence** 💾
  - Replaced direct file write with atomic `.tmp` + `File.Move(..., overwrite: true)` and file-level lock, eliminating 0-byte config corruptions on sudden exit.
- **Legacy Driver Conflicts** 🛡️
  - Completely removed obsolete 2022 `usbip_vhci` driver files to prevent dual-controller conflicts and ensure 100% compatibility with Windows 11 Core Isolation / Memory Integrity.
- **Uninstaller Device Node Cleanup** 🧹
  - Inno Setup uninstaller now removes the `ROOT\USBIP_WIN2\UDE` device node cleanly on uninstallation.

## [2.0.3] - 2025-12-27

### Added
- **Single Instance** 🔒 - Mutex prevents multiple app instances from running
- **Full Translation** 🌐 - Activity Log messages now translate when switching language

### Fixed
- **Tray Icon Cleanup** 🧹 - Fixed ghost tray icon when closing application
- **OnClosing Handler** - Proper disposal of NotifyIcon and ConnectionMonitor

### Added - SnakeUSBIP Server (Windows) 🖥️
- **New Component:** SnakeUSBIP Server - GUI wrapper for usbipd-win
  - Auto-installation of usbipd-win driver (bundled MSI)
  - One-click Share/Stop buttons for USB devices
  - Admin manifest (single UAC prompt at startup)
  - WMI-enriched device names (shows "CruzerBlade" instead of generic)
  - Uninstall option to clean up drivers

### Improved
- **Client Device Names** 📛
  - Now uses `usb.ids` database for descriptive remote device names
  - Shows "SanDisk Corp. : CruzerBlade" instead of generic text

## [2.0.2] - 2025-12-26

### Fixed
- **Auto-Update** 🐛
  - Fixed a critical bug where the application failed to parse release tags from GitHub API due to case sensitivity.
  - Added proper JSON property mapping for reliability.

## [2.0.1] - 2025-12-26

### Improved
- **Notifications** 🔔
  - Implemented hybrid notification system:
    - **Visible Window:** Custom WPF Toast popup (non-intrusive, auto-hides).
    - **Minimized:** Standard Windows BalloonTip (ensures visibility).
  - Notifications no longer accumulate in Windows Action Center.
- **Device Persistence** 💾
  - Application now detects devices that were already connected before startup.
  - Connected devices are prominently displayed with full descriptions.
- **Connection Monitor** ⚡
  - Reduced monitoring interval from 10s to 2s for faster disconnect detection.
  - Improved device matching logic (OR -> AND condition) to avoid false positives.
- **UI UX** ✨
  - Connected devices node now shows full device name and ID (e.g., `1-1: Camera (046d:0825)`).

## [2.0.0] - 2025-12-25

### Added
- **Revamped Architecture (Migration)** 🏗️
  - Complete codebase migration from PowerShell to **.NET 9 (C# / WPF)**.
  - Delivers higher performance, stability, and an ultra-fast native GUI.
- **Rename USB Devices** ✏️
  - New "Rename" context menu in the device list.
  - Allows assigning friendly names (e.g., "Laser Camera") that are persistently saved.
  - Your custom names take precedence over automatic hardware detection.
- **Updated Hardware Database** 📚
  - Updated `usb.ids` to the December 2025 version.
  - Native recognition of +17,000 new devices.
- **Complete x64 Distribution** 📦
  - Available as both **Portable** (ZIP) and **Installer** (EXE).

### Fixed
- **Identification:** Fixed hardware ID conflict for `0bda:5100` (Acmer Camera vs Realtek Adapter).
- **Logging:** Cleanup of redundant activity log messages.
- **Installer:** Fixed installer compilation errors.
