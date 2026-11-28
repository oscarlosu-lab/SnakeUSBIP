# ⚡ Scripts de Automatización y Despliegue de SnakeUSBIP

🌐 **Idioma / Language:** [English](README.md) | **Español**

Este directorio contiene scripts de aprovisionamiento, suites de control y herramientas de automatización multimedia para el ecosistema SnakeUSBIP.

[![Licencia](https://img.shields.io/badge/Licencia-GPLv3-blue.svg?style=flat-square)](https://www.gnu.org/licenses/gpl-3.0)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Apoyar%20Proyecto-FF5E5B?style=flat-square&logo=ko-fi&logoColor=white)](https://ko-fi.com/oscarlosu)

---

## 📜 Índice de Scripts

### 1. `snakeusbip-ctl` — Suite de Control Unificada (macOS y Linux)
Panel interactivo con interfaz TUI para terminal y herramienta de gestión CLI sin dependencias externas.
- **Panel de Control Interactivo (TUI)**: `snakeusbip-ctl` (o `snakeusbip-ctl dashboard`)
- **Modo del Panel**: `snakeusbip-ctl mode [server|client|both]` (se pregunta en el primer arranque; cambiable en cualquier momento con `[m]`)
- **Protección de Suspensión del Cliente opcional (cliente Linux)**: desactivada por defecto. Instalar el script, abrir el panel o conectar dispositivos no instala ni activa ningún servicio. Desde el panel (`[g]`), puedes elegir **Disabled** (desactivada), **Temporary** (activa solo mientras el panel está abierto, se detiene al salir) o **Permanent** (servicio systemd en segundo plano, arranca al iniciar el equipo). Desde CLI: `sudo snakeusbip-ctl client-guard install|uninstall|status`. La conexión y desconexión normal funcionan sin ella. Cuando está activa, escucha `PrepareForSleep` de logind, mantiene un inhibidor de retardo de suspensión, desconecta los dispositivos USB/IP importados antes de suspender (verificado en sysfs de `vhci_hcd`) y los vuelve a conectar al reanudar cuando el servidor responde en TCP 3240. Registros: `journalctl -u snakeusbip-client-guard`. Requiere Linux con systemd/logind, `busctl`, `systemd-inhibit`, `udevadm` y `usbip`. SnakeUSBIP no configura el comportamiento de la tapa.
- **Doctor del Sistema y Diagnóstico JSON**: `snakeusbip-ctl doctor [--json]`, `snakeusbip-ctl status [--json]`
- **Logs**: `snakeusbip-ctl logs` (últimas 100 líneas sin bloqueo) o `snakeusbip-ctl logs -f`
- **Emparejamiento y Túnel TLS 1.3**: `sudo snakeusbip-ctl pair --json`, `sudo snakeusbip-ctl tls-tunnel status`
- **Autoprueba del Protocolo**: `snakeusbip-ctl test`
- **Gestión del Servicio**: `sudo snakeusbip-ctl start|stop|restart|status`
- **Gestión de Dispositivos**: `snakeusbip-ctl list`, `sudo snakeusbip-ctl share <busid>` (desactiva autosuspend USB y soporta `--reset`)
- **Modo Cliente Linux (`vhci_hcd`)**: `snakeusbip-ctl scan|remote <ip>`, `sudo snakeusbip-ctl connect|disconnect|ports`
- **Política de Seguridad (`TCP 3241` y drop-in `bind_address`)**: `sudo snakeusbip-ctl policy show|allow|deny|protect-hid|allow-ip|deny-ip|set-token|clear-token`
- **Parche DualSense para SBCs**: `sudo snakeusbip-ctl fix-dualsense enable|disable|status`

### 2. `snakeusbip-mcp.py` — Servidor MCP JSON-RPC 2.0 por stdio (`v1.4.0`)
Servidor Model Context Protocol en librería estándar de Python con 6 herramientas (`list_devices`, `status`, `share_device`, `unshare_device`, `connect_device`, `disconnect_port`) y aislamiento estricto de `stdout`.

### 2. `install-server-mac.sh` — Instalador 1-Click para macOS
Instalador automático para macOS (Apple Silicon M1-M4 e Intel x86_64).
- Instala el demonio nativo en Swift y el servicio LaunchDaemon.
- Instala `snakeusbip-ctl` en `/usr/local/bin/`.

```bash
curl -fsSL https://raw.githubusercontent.com/oscarlosu-lab/SnakeUSBIP/main/server/scripts/install-server-mac.sh | sudo bash
```

### 3. `install-server-linux.sh` / `install-server.sh` — Instalador 1-Click para Linux y Raspberry Pi
Instalador automático para distribuciones Linux y Raspberry Pi OS (Debian/Ubuntu/Raspbian/Arch/Fedora).
- Carga módulos del núcleo `usbip_core` y `usbip_host`.
- Instala paquete de espacio de usuario `usbip` y servicio systemd.
- Configura regla udev para auto-exportar en caliente.
- Instala `snakeusbip-ctl` en `/usr/local/bin/`.

```bash
curl -fsSL https://raw.githubusercontent.com/oscarlosu-lab/SnakeUSBIP-Server/main/scripts/install-server-linux.sh | sudo bash
```

---

## 📄 Licencia

Licencia GPL-3.0. Desarrollado por [oscarlosu-lab](https://github.com/oscarlosu-lab).
