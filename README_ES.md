# 🌐 USBAnywhere — La Alternativa Libre y Gratuita a VirtualHere para Windows

> *Anteriormente conocido como **SnakeUSBIP***

🌐 **Idioma / Language:** [English](README.md) | **Español**

**v3.0.0** | [Descargar Última Versión](https://github.com/oscarlosu-lab/USBAnywhere/releases/latest) | [📖 Manual de Usuario](docs/USAGE_ES.md) | [🌐 Conexión VPN](docs/VPN_INTERNET_ES.md)

> **¿Por qué pagar 49,00 $ por servidor y estar limitado a un único dispositivo USB?**
> **USBAnywhere** conecta **ilimitados** periféricos USB remotos por LAN, Wi-Fi e Internet con **cero licencias**, **drivers certificados WHQL por Microsoft** y **latencia ultrabaja ajustable**.

Transforma cualquier dispositivo Linux (o PC Windows) en un Hub USB Virtual de alto rendimiento accesible desde Windows 10 y 11. Compatible con **Raspberry Pi, Orange Pi, Banana Pi, Proxmox/HomeLab, Steam Deck, routers OpenWRT, CrealityBox** y cualquier servidor ARM/x86 con Linux.

[![CI Build & Tests](https://github.com/oscarlosu-lab/USBAnywhere/actions/workflows/ci.yml/badge.svg)](https://github.com/oscarlosu-lab/USBAnywhere/actions/workflows/ci.yml)
[![GitHub Downloads](https://img.shields.io/github/downloads/oscarlosu-lab/USBAnywhere/total?style=flat-square&logo=github&color=blue)](https://github.com/oscarlosu-lab/USBAnywhere/releases)
[![GitHub Stars](https://img.shields.io/github/stars/oscarlosu-lab/USBAnywhere?style=flat-square&logo=github&color=yellow)](https://github.com/oscarlosu-lab/USBAnywhere/stargazers)
[![License](https://img.shields.io/github/license/oscarlosu-lab/USBAnywhere?style=flat-square&color=green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11%20(x64%20%26%20ARM64)-lightgrey?style=flat-square&logo=windows)](https://github.com/oscarlosu-lab/USBAnywhere)

---

## ⚔️ ¿Por qué cambiar de VirtualHere a USBAnywhere?

| Característica | **USBAnywhere v3.0** | **VirtualHere** | **USB Network Gate** |
| :--- | :---: | :---: | :---: |
| **Precio y Licencia** | **100% Gratis y Open Source (GPLv3)** | 49,00 USD / Servidor | +159,00 USD |
| **Dispositivos Simultáneos (Free)** | **♾️ Ilimitados** | ⚠️ Solo 1 dispositivo | ❌ Trial limitado |
| **Instalación Servidor en 1-Click** | ✅ **Auto-Instalador SSH Integrado** | ❌ Manual por consola | ❌ Demonio privativo |
| **Modos de Latencia de Red** | ✅ **Dual: Low-Latency WSK y Zero-Copy** | ⚙️ Genérico | ⚙️ Genérico |
| **Interfaz de Usuario** | ✅ **WPF Moderna (Temas Oscuro y Claro)** | 🕰️ Árbol clásico Win98 | 💻 Pesada |
| **Drivers (Windows 10/11)** | ✅ **Certificados WHQL (Soporte HVCI)** | ✅ Firmados | ✅ Firmados |
| **Integración VPN Nativa** | ✅ **Detección Tailscale y ZeroTier** | 💰 Extra / Manual | ❌ Manual |

---

## 🎯 Diseñado para las Comunidades cansadas de Muros de Pago

1. 🎮 **Cloud Gaming, Moonlight / Sunshine y Steam Deck**
   Conecta mandos Xbox/DualSense (con vibración completa, gatillos adaptativos y audio), dongles de auriculares inalámbricos y teclados desde la Raspberry Pi de tu salón directamente a tu PC Gaming.
2. 🏎️ **SimRacing y Simuladores de Vuelo (HOTAS / VR)**
   Conecta volante, pedalera, caja de cambios, botonera y trackers VR simultáneamente por Ethernet usando el modo **Low-Latency WSK** sin pagar licencias por superar 1 dispositivo.
3. 🖨️ **Impresión 3D (Klipper, Mainsail, OctoPrint, CrealityBox)**
   Comparte múltiples cámaras USB, acelerómetros ADXL345 y placas de impresoras 3D sin cables.
4. 🖥️ **HomeLab, Proxmox y Self-Hosted**
   Pasa coordinadores Zigbee/Z-Wave, llaves de seguridad física y dongles de licencia (AutoCAD, iLok, eToken) por LAN o VPN Tailscale.

---

## 🎬 Video Tutorial

<a href="https://www.youtube.com/watch?v=mETEs9INlq4">
  <img src="docs/assets/youtube_thumbnail.png" width="50%" alt="Video Tutorial">
</a>

▶️ **[Ver tutorial completo en YouTube](https://www.youtube.com/watch?v=mETEs9INlq4)**

---

## 🆕 Novedades en v3.0.0 (Evolución a USBAnywhere)

- 🌐 **Nueva marca: USBAnywhere** - Evolución de `SnakeUSBIP` para posicionarse como la alternativa abierta número 1 frente a VirtualHere y VirtualUSB, con migración automática de tu configuración desde v2.x.
- ⚡ **Auto-Instalador SSH en 1-Click** - Convierte cualquier Raspberry Pi, Debian o Ubuntu en un servidor USB/IP listo para usar con un solo botón desde el diálogo SSH.
- ⚡ **Modos Duales de Rendimiento** - Selección entre `zero-copy` (máxima velocidad para almacenamiento y cámaras) y `low-latency` (callbacks WSK en kernel para periféricos HID/gaming/SimRacing).
- 🔌 **Desconexión Limpia al Salir** - Libera automáticamente los puertos USB remotos al cerrar la aplicación, evitando bloqueos en el servidor.
- 🛡️ **Drivers Certificados WHQL** - Controladores oficiales firmados por Microsoft para Windows 10/11 x64 compatibles con Aislamiento de Núcleo (Core Isolation / HVCI).
- 🛠️ **Gestión PnP UDE en Tiempo Real** - Consultas activas de hardware con `pnputil /enum-devices` e instanciación segura sin conflictos con `devnode.exe`.
- 📦 **Modo Portable Híbrido** - Las versiones ZIP guardan la configuración localmente; el instalador usa `%AppData%\USBAnywhere`.
- 📚 **Base de Datos USB Actualizada** - Base `usb.ids` con más de 25.000 dispositivos identificados.

---

## ✨ Características Principales

- 🔍 **Autodescubrimiento** - Escanea servidores USB/IP en tu red local en segundos
- ⚡ **Aprovisionamiento SSH 1-Click** - Instala e inicia `usbipd` en tu Raspberry Pi/Linux automáticamente
- 🌐 **Conexión por Internet** - Conecta desde cualquier lugar vía Tailscale o ZeroTier (NAT traversal)
- ⚡ **Latencia Ajustable** - Modo Zero-Copy de alto ancho de banda o Low-Latency para periféricos sensibles
- 🔌 **Conexión en 1 Click y Desconexión Segura** - Libera puertos automáticamente al cerrar la app
- ⭐ **Favoritos y Auto-Reconexión** - Guarda dispositivos con reconexión automática y perfil de latencia individual
- 📋 **Información de Hardware Detallada** - VID:PID, fabricante y producto de más de 25.000 dispositivos
- 🎨 **GUI Nativa WPF Moderna** - Interfaz fluida en .NET 9 con temas oscuro y claro
- 🌐 **Multi-idioma** - Español e Inglés conmutables en tiempo real
- 🔄 **Auto-actualización Segura** - Descarga e instalación verificada mediante sumas criptográficas SHA-256

---

## 📦 Instalación

### Opción 1: Portable (Sin instalación)
1. Descarga desde [Releases](https://github.com/oscarlosu-lab/USBAnywhere/releases/latest):
   - **Windows x64**: `USBAnywhere-v3.0.0-x64.zip`
   - **Windows ARM64**: `USBAnywhere-v3.0.0-arm64.zip` (Surface Pro X, Snapdragon X Elite, etc.)
2. Extrae el ZIP en cualquier carpeta
3. Ejecuta `USBAnywhere.exe` como Administrador
4. ¡Listo!

### Opción 2: Instalador (x64 Recomendado)
1. Descarga `USBAnywhere_Setup_v3.0.0.exe` desde [Releases](https://github.com/oscarlosu-lab/USBAnywhere/releases/latest)
2. Ejecuta el instalador como Administrador
3. Sigue el asistente de instalación

### ⚠️ Usuarios ARM64
Los drivers ARM64 son **test-signed**. Ver `README_ARM64.md` en el ZIP para instrucciones sobre cómo habilitar Windows Test Mode.

---

## 🚀 Uso Rápido

1. **Escanear** - Click en `🔍 Escanear` para encontrar servidores en tu red
2. **Listar** - Click en `📋 Listar` para ver los dispositivos USB disponibles
3. **Conectar** - Doble-click en un dispositivo o click derecho → Conectar
4. **Desconectar** - Click derecho → Desconectar

### ⚡ Configurar Servidor Linux / Raspberry Pi en 1-Click
1. Haz click en `🔗 SSH` en la barra superior
2. Introduce el usuario de tu Raspberry Pi / Linux (ej. `pi` o `root`) y su IP
3. Pulsa **`⚡ 1-Click Auto-Instalar`** — instalará `usbip`, activará el módulo del kernel de forma persistente, iniciará el demonio y listará tus puertos USB automáticamente.

**O ejecuta el Instalador Plug & Play de 1 Línea en tu Linux / Raspberry Pi:**
```bash
curl -sSL https://raw.githubusercontent.com/oscarlosu-lab/USBAnywhere/main/scripts/install-server.sh | sudo bash
```
> 💡 **100% Plug & Play (¡Igual que VirtualHere!):** Instala `usbipd`, crea el servicio `systemd` y añade una **regla `udev` hotplug** que **auto-exporta automáticamente cualquier USB en cuanto lo enchufas a la Raspberry Pi/Linux**, sin necesidad de escribir `usbip bind` a mano.

### 🐳 Servidor Docker / HomeLab / NAS (`docker-compose.yml`)
Despliega un servidor USB/IP Plug & Play en **Unraid, TrueNAS, Synology o Proxmox** usando [`docker/docker-compose.yml`](docker/docker-compose.yml):
```bash
git clone https://github.com/oscarlosu-lab/USBAnywhere.git && cd USBAnywhere/docker && docker compose up -d
```

### 🎮 Automatización CLI para Moonlight / Sunshine / Playnite
Conecta automáticamente tu mando, volante o auriculares al iniciar un juego en streaming:
```powershell
USBAnywhere.exe --minimized --connect 192.168.1.50 1-1.4
```

### 🌐 Conexión por Internet (VPN)
1. Instala **[Tailscale](https://tailscale.com/download)** en Windows y en tu servidor
2. Click en `📡 VPN` para ver peers con USB/IP activo
3. Selecciona un servidor remoto y conecta

Ver [docs/VPN_INTERNET_ES.md](docs/VPN_INTERNET_ES.md) para la guía completa.

---

## 📁 Estructura

```text
USBAnywhere/
├── USBAnywhere.exe     # Aplicación principal (.NET 9 WPF)
├── usbipw.exe          # Binario cliente USB/IP
├── devnode.exe         # Gestor de nodos PnP UDE
├── libusbip.dll        # Librería core USB/IP
├── drivers/            # Drivers USB/IP certificados WHQL (x64)
├── usb.ids             # Base de datos USB (+25.000 dispositivos)
├── CleanDrivers.ps1    # Utilidad de limpieza de drivers
└── icon.ico            # Icono de la aplicación
```

---

## 📄 Licencia

GPL v3 (GNU General Public License) - Ver [LICENSE](LICENSE)

## 🙏 Créditos

| Proyecto | Autor | Contribución |
|----------|-------|--------------|
| [usbip-win2](https://github.com/vadimgrn/usbip-win2) | **Vadim Grn** | Drivers USB/IP firmados por Microsoft (WHQL certified). Core del cliente Windows. |
| [OctoWrt](https://github.com/ihrapsa/OctoWrt) | **ihrapsa** | Guía original para OpenWrt en CrealityBox. Inspiración para soporte de dispositivos embebidos. |
| [OctoWrt Fork](https://github.com/shivajiva101/OctoWrt) | **ShivaJiva** | Mantenimiento activo de OctoWrt. Releases actualizados para CrealityBox. |
| [USB/IP](https://www.kernel.org/doc/html/latest/usb/usbip_protocol.html) | **Linux Kernel** | Protocolo original USB/IP |
| **USBAnywhere** *(ex-SnakeUSBIP)* | **SnakeFoxu** | GUI .NET 9 WPF, Auto-Setup SSH 1-Click, integración VPN, modos de latencia y documentación |
