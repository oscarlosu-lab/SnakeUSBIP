# 🔒 Política de Privacidad — SnakeUSBIP

🌐 **Language / Idioma:** [English](PRIVACY.md) | **Español**

**Fecha de entrada en vigor:** 1 de noviembre de 2026  
**Proyecto:** SnakeUSBIP (Cliente, Servidor y Android)  
**Responsable:** Oscar Losu ([@oscarlosu-lab](https://github.com/oscarlosu-lab))  
**Licencia:** GNU General Public License v3.0 (GPL-3.0)

[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support%20Project-FF5E5B?style=flat-square&logo=ko-fi&logoColor=white)](https://ko-fi.com/oscarlosu)

---

## 1. Filosofía de Privacidad: Cero Telemetría y Cero Rastreo

Creemos firmemente que las herramientas de software, en particular las utilidades de red y bajo nivel de hardware, deben respetar la privacidad del usuario por diseño.

**SnakeUSBIP está construido bajo una arquitectura estricta de Cero Telemetría (Zero-Telemetry) y Cero Intrusión:**
* **Sin Telemetría**: No recopilamos, monitorizamos, registramos ni transmitimos métricas analíticas, informes de fallos ni datos de diagnóstico a ningún servidor externo.
* **Sin SDKs de Rastreo**: Ningún binario (Windows, macOS, Linux o Android) incluye librerías de seguimiento de terceros (como Google Analytics, Firebase, Sentry, AppCenter o telemetría de Microsoft).
* **Sin Perfiles de Usuario ni Publicidad**: No rastreamos identificadores de hardware, IDs de publicidad ni actividad en línea.
* **Sin Intermediarios en la Nube**: SnakeUSBIP no opera servidores de retransmisión (relay) ni servidores proxy propietarios. Todo el tráfico USB viaja punto a punto (P2P) de forma directa y exclusiva entre tu cliente y tu servidor.

---

## 2. Información Gestionada y Tráfico de Red

### 2.1. Transmisión USB sobre IP (URBs)
* **Qué se transmite:** Bloques de petición USB (URBs), descriptores de dispositivos y datos de control I/O estrictamente necesarios para emular y operar los periféricos USB a través de la red IP.
* **Hacia dónde viaja:** Los datos fluyen **exclusivamente de punto a punto (P2P)** en tu red de área local (LAN) o a través de tu túnel VPN privado, directamente entre el Cliente y el Servidor SnakeUSBIP seleccionados por ti.
* **Seguridad en tránsito:** USB/IP es un protocolo estándar abierto de baja latencia. Al transmitir a través de redes no confiables o Internet público, se recomienda encapsular el tráfico en un túnel seguro cifrado (como WireGuard, OpenVPN o túneles SSH, soportados de forma nativa en la interfaz del Cliente).

### 2.2. Descubrimiento en Red Local (mDNS y Difusión de Subred)
* Al realizar un escaneo de servidores desde la aplicación cliente, SnakeUSBIP emite sondeos de descubrimiento dentro de tu subred local (puerto UDP 3240) o resuelve registros mDNS estándar (`_usbip._tcp.local.`).
* Estos paquetes de descubrimiento **nunca salen de tu red de área local (LAN)**.

### 2.3. Comprobación de Actualizaciones de Software
* Al buscar actualizaciones (manualmente o mediante la opción de comprobación automática), SnakeUSBIP realiza una petición HTTPS GET estándar a la API pública de GitHub:
  `https://api.github.com/repos/oscarlosu-lab/SnakeUSBIP/releases/latest`
* Únicamente se envían las cabeceras HTTP anónimas estándar del sistema operativo a GitHub. No se transmite ningún dato personal, identificador de dispositivo ni estadística de uso.

---

## 3. Almacenamiento Local de Datos

Todas las preferencias del usuario se almacenan de manera local y aislada en tu propio dispositivo:
* **Windows Desktop**: Las configuraciones y favoritos se guardan localmente en `%APPDATA%\SnakeUSBIP\config.json` (o en el directorio de la aplicación en modo Portable).
* **Android**: Las preferencias se guardan exclusivamente en el sandbox de almacenamiento privado de la app (Android DataStore / SQLite). Las copias de seguridad del sistema están explícitamente deshabilitadas (`android:allowBackup="false"`) para impedir extracciones de datos no autorizadas mediante ADB.
* **Linux y macOS**: Almacenado en las rutas estándar XDG (`~/.config/snakeusbip/`).

Ninguna configuración, historial de conexiones ni alias de dispositivos se sube jamás a servidores externos.

---

## 4. Permisos del Sistema Operativo

SnakeUSBIP solicita únicamente los permisos estrictamente indispensables para la comunicación con el hardware:
* **Windows (Permisos de Administrador)**: Requeridos exclusivamente para instalar y comunicarse con el controlador virtual USB/IP (`vhci`) mediante Windows SetupAPI / PnPUtil y vincular sockets de red en puertos protegidos.
* **Android (USB Host y Servicio en Primer Plano)**:
  * `android.permission.FOREGROUND_SERVICE_CONNECTED_DEVICE`: Permite mantener el demonio de servidor USB/IP en ejecución mientras reenvía periféricos en segundo plano.
  * `android.hardware.usb.host`: Permite la comunicación directa con periféricos conectados al puerto USB OTG.
  * **Política Zero-Intrusion**: El inicio automático al arrancar el dispositivo o al conectar un USB viene **deshabilitado por defecto**. SnakeUSBIP nunca se ejecuta en segundo plano sin consentimiento expreso.

---

## 5. Declaración Oficial de Cumplimiento

En conformidad con las directrices de distribución de software y firmas de código abierto (incluidas las directrices de SignPath Foundation y Microsoft Store):

> **Declaración Oficial de Privacidad:**  
> *Este programa no transferirá ninguna información a otros sistemas en red a menos que sea solicitado específicamente por el usuario o la persona que lo instale u opere.*

---

## 6. Transparencia de Código Abierto y Auditoría

La totalidad del código fuente de SnakeUSBIP es público y auditable bajo la licencia **GNU General Public License v3.0**:
* **Repositorio de Código**: [github.com/oscarlosu-lab/SnakeUSBIP](https://github.com/oscarlosu-lab/SnakeUSBIP)
* **Auditorías de Seguridad Continuas**: El código se audita automáticamente mediante GitHub CodeQL (SAST) y análisis de secretos Gitleaks en cada entrega.

---

## 7. Contacto y Soporte

Para cualquier consulta sobre privacidad o seguridad:
* **GitHub Issues**: [github.com/oscarlosu-lab/SnakeUSBIP/issues](https://github.com/oscarlosu-lab/SnakeUSBIP/issues)
* **Autor del Proyecto**: Oscar Losu ([@oscarlosu-lab](https://github.com/oscarlosu-lab))
* **Apoyar el Proyecto**: [ko-fi.com/oscarlosu](https://ko-fi.com/oscarlosu)

