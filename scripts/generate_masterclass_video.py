#!/usr/bin/env python3
"""SnakeUSBIP Masterclass Tutorial Video Generator v2.0 (Bilingual: ES / EN)
Narration powered by ElevenLabs (Voice: oscar asturias via eleven_multilingual_v2) with strict Zero-Waste caching.
Generates 1080p 60fps MP4 tutorial demonstrating 100% of SnakeUSBIP functions.
Usage:
  python generate_masterclass_video.py --lang en
  python generate_masterclass_video.py --lang es
"""
import os
import sys
import json
import time
import subprocess
import urllib.request
import urllib.error
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(REPO_ROOT, "docs")
TEMP_DIR = os.path.join(REPO_ROOT, "release", "temp_masterclass")
ASSETS_DIR = os.path.join(REPO_ROOT, "docs", "assets")
CAPTURES_DIR = os.path.join(ASSETS_DIR, "captures")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Fonts
FONT_REGULAR = r"C:\Windows\Fonts\segoeui.ttf"
FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_CODE = r"C:\Windows\Fonts\consola.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

CONFIG_PATH = os.path.expanduser(r"~/.gemini/config/elevenlabs.json")

def get_elevenlabs_credentials():
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    voice_id = "4HTiOeZanpPrsYjzorSk" # oscar asturias
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                if not api_key:
                    api_key = cfg.get("api_key")
                voice_id = cfg.get("default_voice_id", voice_id)
        except Exception:
            pass
    return api_key, voice_id

SCENES = [
    {
        "id": "scene01_intro",
        "title_es": "SnakeUSBIP v3.0: Arquitectura y Filosofía",
        "title_en": "SnakeUSBIP v3.0: Architecture & Philosophy",
        "subtitle_es": "La alternativa libre, gratuita e ilimitada a VirtualHere",
        "subtitle_en": "The free, unrestricted alternative to VirtualHere",
        "audio_es": (
            "Bienvenidos al tutorial completo de SnakeUSBIP versión 3.0. "
            "A diferencia de soluciones comerciales como VirtualHere, que cobran cuarenta y nueve dólares por servidor "
            "y limitan la versión gratuita a un solo dispositivo, SnakeUSBIP es cien por cien libre, de código abierto "
            "y te permite conectar periféricos USB ilimitados por red local, Wi-Fi o internet con drivers certificados."
        ),
        "audio_en": (
            "Welcome to the comprehensive masterclass tutorial for SnakeUSBIP version 3.0. "
            "Unlike commercial solutions like VirtualHere, which charge forty-nine dollars per server "
            "and limit the free tier to a single device, SnakeUSBIP is one hundred percent free, open source, "
            "and allows you to connect unlimited remote USB devices over LAN, Wi-Fi, or internet with certified drivers."
        ),
        "visual_type": "cards_comparison"
    },
    {
        "id": "scene02_linux_server",
        "title_es": "Servidor Linux y Raspberry Pi en 1-Click",
        "title_en": "1-Click Linux & Raspberry Pi Server Setup",
        "subtitle_es": "Instalación automática y auto-exportación PnP con udev",
        "subtitle_en": "Automated installation and udev hotplug auto-export",
        "audio_es": (
            "Para convertir tu Raspberry Pi o máquina Linux en un servidor USB, solo tienes que ejecutar nuestro instalador oficial en una sola línea. "
            "El script instala los paquetes del kernel, configura el demonio del sistema y activa una regla inteligente en udev. "
            "Gracias a esto, cualquier dispositivo USB que enchufes se comparte al instante en la red de forma totalmente automática."
        ),
        "audio_en": (
            "Turning your Raspberry Pi or Linux machine into a USB server takes just a single command. "
            "Our official one-click installer downloads kernel packages, configures the systemd daemon, and sets up an intelligent udev rule. "
            "Any USB device you plug in is automatically shared over your network with zero manual bind commands required."
        ),
        "visual_type": "terminal_linux"
    },
    {
        "id": "scene03_windows_server",
        "title_es": "SnakeUSBIP Server para Windows",
        "title_en": "SnakeUSBIP Server for Windows",
        "subtitle_es": "Comparte los puertos USB de tu PC con otros equipos",
        "subtitle_en": "Share local USB ports from your PC across your network",
        "audio_es": (
            "Si prefieres compartir dispositivos desde un ordenador con Windows, dispones de SnakeUSBIP Server. "
            "Su interfaz detecta en tiempo real todos los puertos y periféricos locales conectados. "
            "Con un solo clic puedes compartir o desvincular cualquier puerto USB, verificar los registros en vivo "
            "y dejarlo ejecutándose en segundo plano en la bandeja del sistema."
        ),
        "audio_en": (
            "If you prefer sharing devices from a Windows PC, SnakeUSBIP Server has you covered. "
            "Its intuitive interface dynamically detects all connected local USB ports and peripherals. "
            "With a single click, you can share or unshare ports, inspect real-time logs, "
            "and keep it running quietly in the background within your system tray."
        ),
        "visual_type": "windows_server"
    },
    {
        "id": "scene04_installation_drivers",
        "title_es": "Instalación del Cliente y Drivers WHQL",
        "title_en": "Client Installation & WHQL Drivers",
        "subtitle_es": "Instalador Inno Setup con compatibilidad total para Windows 10 y 11",
        "subtitle_en": "Inno Setup installer fully compatible with Windows 10 & 11",
        "audio_es": (
            "En el equipo cliente donde vas a recibir los periféricos, el instalador oficial configura los controladores virtuales certificados por Microsoft. "
            "Es totalmente compatible con Aislamiento de Núcleo e Integridad de Memoria en Windows 10 y 11. "
            "Además, el instalador detecta si la app está en la bandeja del sistema y realiza una instalación o actualización limpia sin conflictos."
        ),
        "audio_en": (
            "On your client PC receiving remote devices, the official installer configures Microsoft WHQL-certified virtual drivers. "
            "It is fully compatible with Core Isolation and Memory Integrity on Windows 10 and 11. "
            "The installer automatically closes running tray instances and guarantees a clean installation without conflicting host nodes."
        ),
        "visual_type": "install_drivers"
    },
    {
        "id": "scene05_network_discovery",
        "title_es": "Autodescubrimiento de Red y Medidor de Ping",
        "title_en": "Network Auto-Discovery & Live Ping Meter",
        "subtitle_es": "Detección UDP en subred local y soporte para redes VPN",
        "subtitle_en": "Subnet UDP detection and seamless VPN support",
        "audio_es": (
            "Al abrir SnakeUSBIP, la aplicación escanea automáticamente tu subred local por UDP y encuentra todos los servidores activos en segundos. "
            "Junto a cada servidor verás un indicador de latencia en milisegundos en tiempo real. "
            "Y si tus equipos están en ubicaciones distintas, puedes añadir servidores remotos manualmente o conectar a través de redes VPN como Tailscale y ZeroTier."
        ),
        "audio_en": (
            "When you launch SnakeUSBIP, it automatically scans your local subnet via UDP and discovers all active servers in seconds. "
            "Next to each server, you will see a live latency meter measuring ping in milliseconds. "
            "You can also add remote servers by manual IP or connect seamlessly across VPN networks like Tailscale and ZeroTier."
        ),
        "visual_type": "discovery_ping"
    },
    {
        "id": "scene06_device_management",
        "title_es": "Gestión de Dispositivos y Auto-Reconexión",
        "title_en": "Device Management & Auto-Reconnect",
        "subtitle_es": "Conexión en 1-click y reconexión automática de favoritos",
        "subtitle_en": "1-click connect and automatic reconnect for favorites",
        "audio_es": (
            "En la lista verás el árbol detallado de periféricos con su nombre comercial gracias a la base de datos de Vendor y Product ID. "
            "Pulsa Conectar para que Windows reconozca el dispositivo como si estuviera pinchado físicamente en tu placa base. "
            "Puedes marcar dispositivos como favoritos para que se reconecten solos al arrancar Windows o tras un corte de alimentación."
        ),
        "audio_en": (
            "In the device list, you will see the full peripheral tree with commercial names from the official vendor ID database. "
            "Simply click Connect, and Windows will recognize the peripheral as if it were plugged directly into your motherboard. "
            "You can also mark favorites to automatically reconnect on Windows startup or after power cycles."
        ),
        "visual_type": "device_tree"
    },
    {
        "id": "scene07_performance_modes",
        "title_es": "Modos de Rendimiento: Low-Latency vs Zero-Copy",
        "title_en": "Performance Tuning: Low-Latency vs Zero-Copy",
        "subtitle_es": "Optimización para Gaming, SimRacing, Moonlight y Cámaras",
        "subtitle_en": "Optimized for Gaming, SimRacing, Moonlight & Webcams",
        "audio_es": (
            "En la barra de estado inferior puedes alternar el perfil de rendimiento. "
            "El modo Low-Latency utiliza callbacks directos en el kernel para eliminar el retardo en mandos y volantes de SimRacing con vibración completa, ideal para Moonlight y Sunshine. "
            "Para cámaras web, grabadoras láser o discos de almacenamiento, el modo Zero-Copy ofrece el máximo ancho de banda."
        ),
        "audio_en": (
            "From the bottom status bar, you can switch performance modes on the fly. "
            "Low-Latency WSK mode uses direct kernel callbacks to eliminate input lag on gamepads and sim-racing wheels with full rumble, making it ideal for Moonlight and Sunshine. "
            "For webcams, laser cutters, or storage drives, Zero-Copy mode provides maximum throughput."
        ),
        "visual_type": "performance_modes"
    },
    {
        "id": "scene08_notifications_tray",
        "title_es": "Notificaciones Nativas y Minimizado a la Bandeja",
        "title_en": "Native Toast Notifications & System Tray",
        "subtitle_es": "Integración con el Centro de Acción de Windows 10 y 11",
        "subtitle_en": "Integrated with Windows 10 & 11 Action Center",
        "audio_es": (
            "SnakeUSBIP se integra con las notificaciones Toast nativas de Windows. "
            "Recibirás avisos claros cuando un dispositivo se conecte, se desconecte o se restablezca el enlace de red. "
            "Al cerrar la ventana, la aplicación se minimiza silenciosamente al área de notificación, consumiendo apenas memoria RAM."
        ),
        "audio_en": (
            "SnakeUSBIP integrates natively with Windows 10 and 11 Toast notifications in the Action Center. "
            "You receive clear visual alerts when devices connect, disconnect, or when network links are restored. "
            "When closed, the application minimizes quietly to the system tray with negligible background memory usage."
        ),
        "visual_type": "notifications_tray"
    },
    {
        "id": "scene09_cli_automation",
        "title_es": "Automatización por Línea de Comandos (CLI)",
        "title_en": "Command-Line Automation (CLI)",
        "subtitle_es": "Lanza conexiones silenciosas con Sunshine o scripts de arranque",
        "subtitle_en": "Launch silent connections with Sunshine or startup scripts",
        "audio_es": (
            "Para entornos avanzados, SnakeUSBIP incluye soporte completo por consola. "
            "Puedes iniciar el ejecutable con el parámetro minimizado y pasarle la IP del servidor y el identificador del bus para conectar tus mandos automáticamente al abrir un juego en Sunshine o Steam Deck, sin necesidad de tocar la interfaz gráfica."
        ),
        "audio_en": (
            "For power users, SnakeUSBIP offers comprehensive command-line automation. "
            "You can launch the executable minimized and pass the server IP and bus ID to attach controllers automatically before starting a game via Sunshine or Steam Deck, without ever touching the graphical user interface."
        ),
        "visual_type": "cli_automation"
    },
    {
        "id": "scene10_summary_community",
        "title_es": "Multidioma Reactivo y Comunidad Open Source",
        "title_en": "Reactive Multi-Language & Open Source Community",
        "subtitle_es": "Español e Inglés dinámico, logs en tiempo real y descarga oficial",
        "subtitle_en": "Dynamic English & Spanish, real-time logs, and official release",
        "audio_es": (
            "Toda la interfaz y los registros son completamente bilingües en español e inglés y cambian al instante sin reiniciar. "
            "SnakeUSBIP es un proyecto comunitario abierto a todos. "
            "Descarga ya el instalador oficial desde nuestro repositorio en GitHub, apoya el proyecto con una estrella y disfruta de la libertad de tus periféricos USB en cualquier lugar."
        ),
        "audio_en": (
            "The interface and structured logs support instant dynamic language switching between English and Spanish. "
            "SnakeUSBIP is a community-driven open-source project. "
            "Download the latest installer from our GitHub repository, support the project with a star, and enjoy unlimited USB peripherals across your network."
        ),
        "visual_type": "summary_community"
    }
]

def generate_audio_elevenlabs(scene, lang, voice_id, api_key):
    scene_id = scene["id"]
    text = scene[f"audio_{lang}"]
    out_path = os.path.join(TEMP_DIR, f"{scene_id}_{lang}.mp3")

    # Strict Zero-Waste Cache check
    if os.path.exists(out_path) and os.path.getsize(out_path) > 2000:
        print(f"  [CACHE HIT] {scene_id}_{lang} already exists ({os.path.getsize(out_path)} bytes). 0 tokens spent.")
        return out_path

    print(f"  [SYNTHESIZING] {scene_id} ({len(text)} chars | {lang.upper()}) with voice 'oscar asturias'...")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.50,
            "similarity_boost": 0.85,
            "style": 0.15,
            "use_speaker_boost": True
        }
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        }
    )
    with urllib.request.urlopen(req) as resp:
        audio_bytes = resp.read()
        with open(out_path, "wb") as f:
            f.write(audio_bytes)
    print(f"  [SAVED] {out_path} ({len(audio_bytes)} bytes)")
    return out_path

def get_audio_duration(file_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", file_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def create_slide_image(scene, lang, out_path):
    w, h = 1920, 1080
    im = Image.new("RGB", (w, h), color="#0F172A")
    draw = ImageDraw.Draw(im)

    # Accent Header Bar
    draw.rectangle([(0, 0), (w, 12)], fill="#06B6D4")

    # Brand header
    draw.text((80, 50), "🌐 SnakeUSBIP", font=get_font(FONT_BOLD, 32), fill="#06B6D4")
    badge_text = "•  Masterclass Tutorial  •  v3.0.0 Official" if lang == "en" else "•  Masterclass Tutorial  •  v3.0.0 Oficial"
    draw.text((360, 56), badge_text, font=get_font(FONT_BOLD, 22), fill="#94A3B8")

    # Title & Subtitle
    draw.text((80, 120), scene[f"title_{lang}"], font=get_font(FONT_BOLD, 50), fill="#F8FAFC")
    draw.text((80, 190), scene[f"subtitle_{lang}"], font=get_font(FONT_REGULAR, 26), fill="#38BDF8")

    vtype = scene["visual_type"]

    if vtype == "cards_comparison":
        # Card 1: VirtualHere
        draw.rounded_rectangle([(80, 270), (920, 920)], radius=20, fill="#1E293B", outline="#475569", width=2)
        draw.text((120, 310), "❌ VirtualHere", font=get_font(FONT_BOLD, 36), fill="#EF4444")
        vh_pts = [
            "• $49.00 USD per server license",
            "• Free tier limited to only 1 device",
            "• Manual Linux command-line setup",
            "• Outdated UI without touch/fluent design",
            "• Closed-source proprietary software"
        ] if lang == "en" else [
            "• Licencia de 49,00 $ por servidor",
            "• Versión gratis limitada a 1 solo dispositivo",
            "• Configuración manual en Linux sin hotplug",
            "• Interfaz obsoleta sin soporte táctil",
            "• Software privativo de código cerrado"
        ]
        y = 400
        for pt in vh_pts:
            draw.text((120, y), pt, font=get_font(FONT_REGULAR, 26), fill="#CBD5E1")
            y += 80

        # Card 2: SnakeUSBIP
        draw.rounded_rectangle([(1000, 270), (1840, 920)], radius=20, fill="#0F2D37", outline="#06B6D4", width=3)
        draw.text((1040, 310), "✅ SnakeUSBIP v3.0", font=get_font(FONT_BOLD, 36), fill="#10B981")
        ua_pts = [
            "• 100% Free & Open Source (GPLv3)",
            "• Unlimited simultaneous devices",
            "• 1-Click Plug & Play Linux auto-installer",
            "• Automatic hotplug udev export in real time",
            "• Microsoft WHQL-certified drivers (HVCI ready)",
            "• Native Client & Server for Windows 10/11"
        ] if lang == "en" else [
            "• 100% Gratuito y Open Source (GPLv3)",
            "• Dispositivos simultáneos ilimitados",
            "• Instalador 1-Click para Raspberry Pi y Linux",
            "• Auto-exportación Plug & Play inmediata con udev",
            "• Drivers WHQL de Microsoft (HVCI compatible)",
            "• Cliente y Servidor nativos para Windows 10/11"
        ]
        y = 390
        for pt in ua_pts:
            draw.text((1040, y), pt, font=get_font(FONT_REGULAR, 25), fill="#F1F5F9")
            y += 72

    elif vtype == "terminal_linux":
        draw.rounded_rectangle([(80, 270), (1840, 920)], radius=20, fill="#020617", outline="#334155", width=2)
        draw.ellipse([(110, 295), (130, 315)], fill="#EF4444")
        draw.ellipse([(145, 295), (165, 315)], fill="#F59E0B")
        draw.ellipse([(180, 295), (200, 315)], fill="#10B981")
        draw.text((220, 294), "terminal: raspberrypi ~ snakeusbip server setup", font=get_font(FONT_REGULAR, 20), fill="#64748B")

        draw.text((120, 360), "$ curl -sSL https://raw.githubusercontent.com/oscarlosu-lab/SnakeUSBIP/main/scripts/install-server.sh | sudo bash", font=get_font(FONT_CODE, 24), fill="#38BDF8")
        term_output = [
            "[1/4] Installing USB/IP kernel packages (usbip, hwdata, usbutils)... [OK]",
            "[2/4] Enabling kernel modules in /etc/modules-load.d/usbip.conf... [OK]",
            "[3/4] Installing Plug & Play Auto-Bind engine to /usr/local/bin/snakeusbip-autobind.sh...",
            "[4/4] Creating systemd service (snakeusbip.service) and udev hotplug rules...",
            "      --> udev rules reloaded: any USB device plugged in will be automatically exported!",
            "",
            "✅ SnakeUSBIP Server is active and listening on TCP port 3240!",
            "🔌 Plug & Play Auto-Export is ACTIVE: zero manual bind commands required."
        ] if lang == "en" else [
            "[1/4] Instalando paquetes USB/IP del kernel (usbip, hwdata, usbutils)... [OK]",
            "[2/4] Activando modulos del kernel en /etc/modules-load.d/usbip.conf... [OK]",
            "[3/4] Instalando motor de Auto-Bind Plug & Play en /usr/local/bin/snakeusbip-autobind.sh...",
            "[4/4] Creando servicio systemd (snakeusbip.service) y reglas de udev hotplug...",
            "      --> Reglas udev recargadas con exito: cualquier USB enchufado se compartira solo.",
            "",
            "✅ SnakeUSBIP Server activo y escuchando en el puerto TCP 3240!",
            "🔌 Plug & Play Auto-Export ACTIVO: no se requieren comandos bind manuales."
        ]
        y = 440
        for line in term_output:
            c = "#10B981" if "✅" in line or "ACTIVE" in line or "ACTIVO" in line or "[OK]" in line else "#94A3B8"
            draw.text((120, y), line, font=get_font(FONT_CODE, 22), fill=c)
            y += 50

    else:
        cap_file = None
        if vtype in ("discovery_ping", "device_tree"):
            cap_file = os.path.join(CAPTURES_DIR, "capture_01_mainwindow_dark.png")
        elif vtype == "performance_modes":
            cap_file = os.path.join(CAPTURES_DIR, "capture_04_mainwindow_light.png")
        elif vtype == "notifications_tray":
            cap_file = os.path.join(ASSETS_DIR, "app_frame.png")
        elif vtype == "cli_automation":
            cap_file = os.path.join(CAPTURES_DIR, "capture_01_mainwindow_dark.png")
        else:
            cap_file = os.path.join(ASSETS_DIR, "app_frame.png")

        if cap_file and os.path.exists(cap_file):
            try:
                cap_im = Image.open(cap_file)
                cap_im.thumbnail((840, 640), Image.Resampling.LANCZOS)
                im.paste(cap_im, (80, 270))
            except Exception as e:
                print("Image paste error:", e)
        else:
            draw.rounded_rectangle([(80, 270), (920, 920)], radius=20, fill="#1E293B", outline="#334155", width=2)
            draw.text((120, 310), "🖥️ SnakeUSBIP UI", font=get_font(FONT_BOLD, 32), fill="#38BDF8")

        draw.rounded_rectangle([(960, 270), (1840, 920)], radius=20, fill="#1E293B", outline="#0EA5E9", width=2)
        font_h = get_font(FONT_BOLD, 32)
        font_b = get_font(FONT_REGULAR, 23)

        if vtype == "windows_server":
            h_text = "💻 Native Windows Server" if lang == "en" else "💻 Servidor Nativo Windows"
            pts = [
                "• Dynamic PnP detection of local USB ports",
                "• 1-Click Share & Unshare buttons",
                "• No console commands or reboot required",
                "• Silent background minimization to System Tray",
                "• Continuous background service execution",
                "• Real-time connection history and structured logs"
            ] if lang == "en" else [
                "• Detección PnP dinámica de puertos USB locales",
                "• Botón Compartir / Descompartir en 1 clic",
                "• No requiere comandos de consola ni reiniciar",
                "• Minimizado silencioso al System Tray",
                "• Ejecución continua como servicio de fondo",
                "• Historial de conexiones y registros en vivo"
            ]
        elif vtype == "install_drivers":
            h_text = "🛡️ Certified WHQL Drivers" if lang == "en" else "🛡️ Drivers WHQL Certificados"
            pts = [
                "• Professional Inno Setup installer package",
                "• Full Core Isolation & Memory Integrity (HVCI) support",
                "• Automatic detection and clean shutdown of running instances",
                "• Safe cleanup of legacy virtual adapter nodes",
                "• Portable standalone version (no admin required)",
                "• Native binaries for x64 and Windows ARM64"
            ] if lang == "en" else [
                "• Paquete de instalación profesional Inno Setup",
                "• Compatibilidad con Aislamiento de Núcleo (HVCI)",
                "• Detección y cierre limpio de instancias previas",
                "• Limpieza segura de adaptadores virtuales antiguos",
                "• Versión portable standalone (sin necesidad de admin)",
                "• Binarios nativos para x64 y Windows ARM64"
            ]
        elif vtype == "discovery_ping":
            h_text = "⚡ Network & Discovery" if lang == "en" else "⚡ Descubrimiento y Red"
            pts = [
                "• Automatic UDP broadcast scan across local subnet",
                "• Instant server discovery without manual IP setup",
                "• Real-time ping latency badge (e.g. ⚡ 0.8 ms)",
                "• 'Add Server' button for static remote IP addresses",
                "• Seamless support for Tailscale, ZeroTier, & WireGuard",
                "• Remote access via integrated secure SSH tunnels"
            ] if lang == "en" else [
                "• Escaneo UDP automático en la subred local",
                "• Detección instantánea de servidores sin configurar IPs",
                "• Medidor de ping en tiempo real (ej. ⚡ 0.8 ms)",
                "• Botón 'Añadir Servidor' manual para IPs fijas",
                "• Compatibilidad con Tailscale, ZeroTier y WireGuard",
                "• Acceso remoto a través de túneles SSH integrados"
            ]
        elif vtype == "device_tree":
            h_text = "🔌 Peripheral Management" if lang == "en" else "🔌 Gestión de Periféricos"
            pts = [
                "• Commercial names via official usb.ids database",
                "• Displays Vendor ID, Product ID, and USB 2.0/3.0 speeds",
                "• Instant 1-click Connect & Disconnect",
                "• 'Auto-connect' checkbox for startup favorites",
                "• Fault-tolerant auto-reconnect on power resets",
                "• Native audio volume and haptic rumble pass-through"
            ] if lang == "en" else [
                "• Nombres comerciales reales vía base usb.ids",
                "• Muestra Vendor ID, Product ID y velocidad (USB 2.0/3.0)",
                "• Conexión y desconexión instantánea en 1 clic",
                "• Casilla 'Auto-conectar' para favoritos de arranque",
                "• Reconexión automática tolerante a cortes eléctricos",
                "• Control de volumen y respuesta háptica nativa"
            ]
        elif vtype == "performance_modes":
            h_text = "🎮 Performance Profiles" if lang == "en" else "🎮 Modos de Rendimiento"
            pts = [
                "🏎️ LOW-LATENCY WSK MODE:",
                "   • Direct kernel-level event callbacks",
                "   • Zero input lag for gamepads, SimRacing wheels & pedals",
                "   • Perfect match for Moonlight, Sunshine & Steam Deck",
                "📹 ZERO-COPY MODE:",
                "   • Maximum network bandwidth without intermediate buffers",
                "   • Ideal for UVC webcams, laser cutters, 3D printers & drives"
            ] if lang == "en" else [
                "🏎️ MODO LOW-LATENCY (WSK):",
                "   • Callbacks directos en el kernel de Windows",
                "   • Cero retardo en mandos, volantes SimRacing y pedales",
                "   • Soporte perfecto para Moonlight, Sunshine y Steam Deck",
                "📹 MODO ZERO-COPY:",
                "   • Máximo ancho de banda de red sin copias intermedias",
                "   • Ideal para cámaras web UVC, grabadoras láser y discos"
            ]
        elif vtype == "notifications_tray":
            h_text = "🔔 Notifications & Tray" if lang == "en" else "🔔 Notificaciones y Bandeja"
            pts = [
                "• Native Windows 10/11 Toast notifications",
                "• Alerts on connect, disconnect, and network recovery",
                "• Integrated into Windows Action Center",
                "• Quiet minimization to system tray with status icon",
                "• Quick context menu to attach or detach peripherals",
                "• Ultra-low background memory footprint"
            ] if lang == "en" else [
                "• Notificaciones Toast nativas en Windows 10 y 11",
                "• Avisos de conexión, desconexión y pérdida de enlace",
                "• Integradas en el Centro de Acción del sistema",
                "• Minimizado al System Tray con icono de estado",
                "• Menú contextual rápido para conectar y desconectar",
                "• Consumo ultra-reducido de memoria en segundo plano"
            ]
        elif vtype == "cli_automation":
            h_text = "🤖 CLI Automation" if lang == "en" else "🤖 Automatización por CLI"
            pts = [
                "• Command-line flags for automation scripts:",
                "   SnakeUSBIP.exe --minimized --connect <IP> <BUSID>",
                "• Seamless Sunshine & Moonlight Game Streaming integration",
                "• Auto-attach in Sunshine preparation commands",
                "• Automatic detach when streaming session ends",
                "• Compatible with Playnite, Steam launchers, and batch files"
            ] if lang == "en" else [
                "• Parámetros por línea de comandos para scripts:",
                "   SnakeUSBIP.exe --minimized --connect <IP> <BUSID>",
                "• Integración con Sunshine / Moonlight Game Streaming",
                "• Auto-conexión en comandos prep antes de lanzar juegos",
                "• Desconexión automática al cerrar la sesión",
                "• Compatible con lanzadores Playnite, Steam y scripts .bat"
            ]
        elif vtype == "summary_community":
            h_text = "🌐 Multi-Language & Community" if lang == "en" else "🌐 Multidioma y Comunidad"
            pts = [
                "• 100% bilingual UI & structured logs (English & Spanish)",
                "• Reactive log viewer with live event filtering",
                "• 100% Free & Open Source under GPLv3 license",
                "• Official release downloads on GitHub Releases",
                "• Compatible with Winget, Scoop, and Docker",
                "• ⭐ Support the project with a star on GitHub!"
            ] if lang == "en" else [
                "• Interfaz y logs 100% bilingües en tiempo real (ES / EN)",
                "• Formato de logs reactivo con visor de eventos integrado",
                "• 100% Código Abierto con licencia GPLv3",
                "• Descargas oficiales en GitHub Releases",
                "• Compatible con Winget, Scoop y Docker",
                "• ⭐ ¡Apoya el proyecto con una estrella en GitHub!"
            ]

        draw.text((1000, 310), h_text, font=font_h, fill="#38BDF8")
        y = 390
        for pt in pts:
            col = "#F1F5F9" if not pt.startswith("🏎️") and not pt.startswith("📹") else ("#38BDF8" if "LOW" in pt else "#F59E0B")
            draw.text((1000, y), pt, font=font_b, fill=col)
            y += 56

    im.save(out_path)
    return out_path

def generate_srt(scene_durations, srt_path, lang):
    def format_ts(seconds):
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

    current = 0.0
    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, (scene, dur) in enumerate(scene_durations, 1):
            start = current
            end = current + dur
            text = scene[f"audio_{lang}"]
            f.write(f"{idx}\n")
            f.write(f"{format_ts(start)} --> {format_ts(end)}\n")
            f.write(f"{text}\n\n")
            current = end

def build_masterclass_video(lang="es"):
    api_key, voice_id = get_elevenlabs_credentials()
    if not api_key:
        print("\033[91m[!] Error: No ElevenLabs API key found.\033[0m")
        sys.exit(1)

    print("════════════════════════════════════════════════════════════════════")
    print(f" 🎬 SnakeUSBIP Masterclass Video Generator [{lang.upper()}]")
    print(f" 🎙️ Narration: oscar asturias (ID: {voice_id}) via Multilingual v2")
    print(" 🛡️ Protocol: Zero-Waste ElevenLabs (Strict Disk Caching)")
    print("════════════════════════════════════════════════════════════════════\n")

    total_chars = sum(len(s[f"audio_{lang}"]) for s in SCENES)
    print(f"[*] Total scenes: {len(SCENES)}")
    print(f"[*] Total script characters: {total_chars:,} characters\n")

    scene_clips = []
    scene_durations = []

    for idx, scene in enumerate(SCENES, 1):
        sid = scene["id"]
        print(f"[{idx}/{len(SCENES)}] Processing scene: {sid} [{lang.upper()}]...")

        # 1. Audio (ElevenLabs with cache check)
        audio_file = generate_audio_elevenlabs(scene, lang, voice_id, api_key)
        duration = get_audio_duration(audio_file)
        padded_duration = duration + 0.5
        scene_durations.append((scene, padded_duration))
        print(f"      Audio duration: {duration:.2f}s (Clip: {padded_duration:.2f}s)")

        # 2. Slide image
        slide_img = os.path.join(TEMP_DIR, f"{sid}_{lang}.png")
        create_slide_image(scene, lang, slide_img)

        # 3. Render video clip individual
        clip_path = os.path.join(TEMP_DIR, f"{sid}_{lang}.mp4")
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", slide_img,
            "-i", audio_file,
            "-c:v", "libx264", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
            "-pix_fmt", "yuv420p",
            "-t", str(padded_duration),
            "-shortest",
            clip_path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[!] ffmpeg error in {sid}: {res.stderr}")
            sys.exit(1)
        scene_clips.append(clip_path)

    # 4. SRT Subtitles
    srt_output = os.path.join(OUTPUT_DIR, f"SnakeUSBIP_Masterclass_Tutorial_{lang.upper()}.srt")
    generate_srt(scene_durations, srt_output, lang)
    print(f"\n[✓] Subtitles generated: {srt_output}")

    # 5. Concatenate
    concat_list = os.path.join(TEMP_DIR, f"concat_list_{lang}.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        for c in scene_clips:
            clean_path = c.replace("\\", "/")
            f.write(f"file '{clean_path}'\n")

    final_video = os.path.join(OUTPUT_DIR, f"SnakeUSBIP_Masterclass_Tutorial_{lang.upper()}.mp4")
    print(f"\n[*] Rendering final 1080p video with ffmpeg: {final_video}...")
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list,
        "-c", "copy",
        final_video
    ]
    res = subprocess.run(concat_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[!] Error concatenating final video: {res.stderr}")
        sys.exit(1)

    # Copy to release
    release_video = os.path.join(REPO_ROOT, "release", f"SnakeUSBIP_Masterclass_Tutorial_{lang.upper()}.mp4")
    release_srt = os.path.join(REPO_ROOT, "release", f"SnakeUSBIP_Masterclass_Tutorial_{lang.upper()}.srt")
    try:
        import shutil
        shutil.copyfile(final_video, release_video)
        shutil.copyfile(srt_output, release_srt)
    except Exception as e:
        print(f"Notice copying to release: {e}")

    final_duration = get_audio_duration(final_video)
    final_size_mb = os.path.getsize(final_video) / (1024 * 1024)
    print(f"\n🎉 SUCCESS! MASTERCLASS VIDEO [{lang.upper()}] GENERATED!")
    print(f"   🎥 Video: {final_video}")
    print(f"   ⏱️ Duration: {final_duration:.1f}s ({final_duration/60:.2f} min)")
    print(f"   📦 Size: {final_size_mb:.2f} MB")
    print(f"   📄 Subtitles: {srt_output}")

if __name__ == "__main__":
    lang = "en"
    if len(sys.argv) > 1 and sys.argv[1] in ("--lang", "-l") and len(sys.argv) > 2:
        lang = sys.argv[2].lower()
    elif len(sys.argv) > 1 and sys.argv[1].lower() in ("es", "en"):
        lang = sys.argv[1].lower()
    build_masterclass_video(lang)
