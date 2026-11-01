<div align="center">

# 🐍 SnakeUSBIP v3.0

**La alternativa libre y gratuita a VirtualHere para Windows, Android, macOS y Linux**

[![License: GPL v3](https://img.shields.io/badge/Licencia-GPLv3-blue.svg?style=flat-square)](https://www.gnu.org/licenses/gpl-3.0)
[![.NET 9.0](https://img.shields.io/badge/.NET-9.0-purple.svg?style=flat-square&logo=dotnet)](https://dotnet.microsoft.com/)
[![Plataformas](https://img.shields.io/badge/Plataformas-Windows%20%7C%20Android%20%7C%20macOS%20%7C%20Linux-green.svg?style=flat-square)]()
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support%20Project-FF5E5B?style=flat-square&logo=ko-fi&logoColor=white)](https://ko-fi.com/oscarlosu)

[English](README.md) | [Español](README_ES.md)

</div>

---

## 🌐 Visión General

**SnakeUSBIP** es una suite multiplataforma unificada de USB sobre IP diseñada para conectar dispositivos USB ilimitados a través de LAN, Wi-Fi e Internet con latencia ultrabaja. Ofrece una alternativa completa, moderna y 100% gratuita a herramientas comerciales como VirtualHere.

### ✨ Características Principales
- **Cliente Visual (Windows WPF)**: Interfaz moderna, autodescubrimiento por red (mDNS), conexión en un clic, reconexión automática y soporte de múltiples servidores.
- **Servidor Unificado (.NET 9 / CLI / Swift)**: Demonio USB/IP de alto rendimiento para Windows, Linux (`snakeusbip-ctl`) y macOS Apple Silicon nativo.
- **Servidor Android sin Root**: Convierte cualquier móvil, tablet o Android TV en un servidor USB/IP sin necesidad de root. Soporte para Sunshine con hápticos DualSense y Force Feedback (FFB) para volantes de simulación.
- **Seguridad e Integridad**: Compilación nativa, verificación criptográfica SHA-256 y cero telemetría.

---

## 📁 Estructura del Monorepo

```text
SnakeUSBIP/
├── client/          # Cliente WPF y controlador de bandeja para Windows
├── server/          # Servidor multiplataforma (.NET 9 Windows, Swift macOS, Linux CLI)
├── android/         # Aplicación y servidor sin root para Android / Android TV
├── tools/           # Automatización de compilación y empaquetado seguro
├── docs/            # Documentación técnica completa y guías de uso
├── docker/          # Servidor USB/IP linux en contenedor Docker
└── SnakeUSBIP.sln   # Solución unificada de Visual Studio / .NET
```

---

## 🚀 Inicio Rápido y Compilación

### Requisitos
- [.NET 9.0 SDK](https://dotnet.microsoft.com/download/dotnet/9.0)
- Java 17+ y Android SDK (para compilar la app Android)

### 1. Compilar Cliente y Servidor (.NET 9)
```powershell
dotnet restore SnakeUSBIP.sln
dotnet build SnakeUSBIP.sln -c Release
dotnet test SnakeUSBIP.sln -c Release
```

### 2. Compilar la App Android
```bash
cd android
./gradlew assembleRelease
```

---

## ☕ Apoyo Comunitario

SnakeUSBIP es software 100% gratuito y de código abierto bajo la licencia **GNU General Public License v3 (GPLv3)**. Si SnakeUSBIP te es de utilidad, puedes apoyar su mantenimiento continuado:

[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support%20Project-FF5E5B?style=flat-square&logo=ko-fi&logoColor=white)](https://ko-fi.com/oscarlosu)

---

## ⚖️ Licencia y Marca

- **Licencia**: [GNU General Public License v3](LICENSE).
- **Aviso de Marca**: SnakeUSBIP es un proyecto de código abierto desarrollado y mantenido por `oscarlosu-lab`.
