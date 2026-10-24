# CHANGELOG - USBAnywhere (Formerly SnakeUSBIP)

## [3.0.0] - 2026-10-24

### Added
- **Major Brand Evolution: USBAnywhere** 🌐
  - Rebranded from `SnakeUSBIP` to **`USBAnywhere`** — positioned as the premier free, open-source alternative to VirtualHere, VirtualUSB, and USB Network Gate.
  - Updated executable (`USBAnywhere.exe`), installer (`USBAnywhere_Setup_v3.0.0.exe`), portable packages, UI header, system tray, and logs (`usbanywhere_YYYYMMDD.log`).
- **1-Click SSH Server Auto-Setup** ⚡
  - Added `⚡ 1-Click Auto-Setup` inside the SSH configuration dialog to automatically provision Raspberry Pi / Debian / Ubuntu servers (`apt install usbip hwdata usbutils`, persistent `usbip_host` kernel module in `/etc/modules`, and `usbipd -D` daemon start).
- **Seamless Legacy Configuration Migration** 🔄
  - Automatically migrates existing user settings and favorites from `%AppData%\SnakeUSBIP\config.json` to `%AppData%\USBAnywhere\config.json` on first startup.

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

---

## [1.8.0] - 2025-12-24

### Maintenance
- **Legacy Release** 📦
  - Versión final basada en PowerShell (v1.x)
  - Congelada para migración a v2.0 (WPF)
  - Limpieza final de repositorio y dependencias

## [1.7.3] - 2025-12-20

### Changed
- **Default language is now English** 🌐
  - App starts in English by default (was Spanish)
  - Spanish-speaking users can switch with one click
- **Language button shows flag emojis** 🇬🇧🇪🇸
  - `🇬🇧 EN` for English, `🇪🇸 ES` for Spanish
  - Clearer visual indicator of current language

---

## [1.7.2] - 2025-12-19

### Añadido
- **Botón "Añadir Todos" en diálogo VPN** ➕
  - Nuevo botón verde que añade todos los servidores VPN con USB/IP activo
  - Permite conectar múltiples servidores Tailscale/ZeroTier de golpe

### Corregido
- **Escaneo de red local separado de VPN** 🔍
  - El botón "Escanear" ahora solo busca en la red LOCAL (192.168.x.x, etc.)
  - Excluye automáticamente subredes de Tailscale (100.64.0.0/10)
  - Para buscar servidores VPN, usar el botón "🌐 VPN"
- **Botón VPN ahora lista dispositivos** 🔗
  - Al seleccionar un peer y pulsar "Conectar", se listan sus dispositivos en el TreeView
  - Ya no es necesario escribir manualmente la IP del servidor VPN

---

## [1.7.0] - 2025-12-19

### Añadido
- **Botón VPN / Internet** 🌐
  - Nuevo botón "🌐 VPN" para conexión remota por Internet
  - Detecta automáticamente Tailscale y ZeroTier instalados
  - Escanea peers VPN buscando servidores USB/IP activos
  - Dialog con lista de peers y estado de conexión
  - Conectar directamente a servidores USB/IP remotos
- **Traducciones VPN**
  - Nuevas cadenas en español e inglés para la funcionalidad VPN
- **Interfaz más ancha**
  - Formulario principal ampliado de 520 a 590 píxeles
  - Espacio para nuevo botón sin afectar diseño existente

### Cambiado
- Ajustados anchos de TreeView, LogPanel y ServerPanel

---

## [1.6.1] - 2025-12-18

### Añadido
- **Log de Actividad** 📋
  - Panel con historial de eventos
  - Registra conexiones, desconexiones, escaneos y errores
  - Botón para limpiar historial
  - Timestamps en cada entrada

### Corregido
- **Escaneo inicial** 🐛
  - Ahora encuentra todos los servidores desde el arranque
  - Solucionado problema de concurrencia en callbacks
- **Timeout de escaneo** ⏱️
  - Aumentado de 100ms a 300ms para servidores lentos

---

## [1.6.0] - 2025-12-10

### Añadido
- **Interfaz estilo macOS** 🍎
  - Botones de ventana redondos (🟡🟢🔴)
  - Sin barra de Windows (custom title bar)
  - Arrastrar ventana desde barra de título
- **Estilos mejorados** ✨
  - Botones con efectos hover
  - Colores vibrantes y modernos
  - Zorro naranja en el título
- **Traducciones mejoradas** 🌐
  - Más elementos se traducen al cambiar idioma
  - TreeView y labels actualizados

---

## [1.5.0] - 2025-12-10

### Añadido
- **Multi-idioma** 🌐
  - Español (ESP) e Inglés (ENG)
  - Botón selector en barra de título
  - Se guarda preferencia en config
- **Auto-actualización** ⬆️
  - Comprueba versión en GitHub
  - Descarga e instala automáticamente

### Cambiado  
- Botón cerrar (X) ahora cierra la aplicación
- Botón minimizar sigue enviando a bandeja del sistema

---

## [1.4.0.0] - 2025-12-10

### Añadido
- **Múltiples Servidores Simultáneos** 🎉
  - Escaneo encuentra TODOS los servidores en la subred
  - TreeView muestra múltiples servidores al mismo tiempo

---

## [1.3.0.0] - 2025-12-10

### Añadido
- **System Tray (Bandeja del sistema)** 🎉
  - Ícono en la bandeja del sistema con el logo de SnakeFoxU
  - Minimizar a tray (al minimizar o cerrar la ventana)
  - Menú contextual: Escanear Red, Mostrar Ventana, Salir
  - Doble-click en ícono restaura la ventana
  - Notificación balloon al minimizar
  - La app sigue corriendo en segundo plano

---

## [1.2.0.0] - 2025-12-09

### Añadido
- **Contador de dispositivos** - Muestra "(X)" junto a cada nodo del TreeView
  - `📡 USB Hubs (3)` - Total de dispositivos remotos
  - `🖥️ 192.168.1.100 (3)` - Dispositivos por servidor
  - `✅ Dispositivos Conectados (2)` - Dispositivos USB/IP activos
  - `⭐ Favoritos (1)` - Total de favoritos guardados
- **Tooltips** - Info detallada al pasar el mouse sobre dispositivos
  - Dispositivos remotos: Bus ID, VID:PID, Fabricante, Producto, Servidor
  - Dispositivos conectados: Puerto, Producto, Servidor remoto
  - Favoritos: Bus ID, Servidor, Auto-conectar (Sí/No)

---


## [1.0.0.0] - 2025-12-09 (Release)

### 🎉 Versión 1.0 - Release Oficial

#### Funcionalidades Principales
- **GUI estilo VirtualHere** - TreeView jerárquico con menú contextual
- **Autodescubrimiento** - Escaneo automático de servidores en subred local
- **Conexión/Desconexión USB/IP** - Gestión completa de dispositivos remotos
- **Sistema de Favoritos** - Guardar dispositivos con reconexión automática
- **Botón SSH** - Configurar servidor USB/IP en Raspberry Pi
- **Información VID:PID** - Datos extendidos de fabricante/producto
- **Instalación de Drivers** - Botones para instalar/desinstalar drivers USB/IP
- **Portable** - Versión lista para distribuir

#### Archivos Incluidos
- `SnakeUSBIP.exe` - Aplicación principal
- `usbipw.exe` - Cliente USB/IP
- `devnode.exe` - Gestor de nodos de dispositivo
- `usb.ids` - Base de datos de fabricantes USB
- `drivers/` - Drivers USB/IP para Windows

---

### Pendiente (Futuras versiones)
- [ ] Notificaciones (conexión/desconexión)
- [ ] Log de actividad
- [x] ~~Ícono en bandeja del sistema (System Tray)~~ ✅ v1.3.0
- [ ] Soporte múltiples servidores simultáneos

---

## Historial de Desarrollo

### Pre-release
- v1.1.0: Botón "Ver Conectados", instalación de drivers
- v1.2.0: Feature 2 - Información VID:PID
- v1.3.0: GUI estilo VirtualHere (TreeView)
- v1.4.0: Feature 3 - Sistema de Favoritos
- v1.5.0: Botón SSH para Raspberry Pi
- v1.5.1: Fix popups 0,1,2 al iniciar
