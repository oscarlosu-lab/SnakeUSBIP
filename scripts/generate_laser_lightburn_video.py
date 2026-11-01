#!/usr/bin/env python3
"""SnakeUSBIP Laser & LightBurn Masterclass Video Generator (Bilingual: ES / EN)
Narration: ElevenLabs ('oscar asturias' via eleven_multilingual_v2) with strict Zero-Waste caching and local fallback.
Renders high-definition 1080p 60fps MP4 video + synchronized .srt subtitles.
Specifically focuses on: Diode Laser (GRBL/Ruida) + LightBurn Camera over Wi-Fi/LAN/VPN.

Usage:
  python generate_laser_lightburn_video.py --lang es
  python generate_laser_lightburn_video.py --lang en
  python generate_laser_lightburn_video.py --all
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
TEMP_DIR = os.path.join(REPO_ROOT, "release", "temp_laser_video")
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
        "id": "scene01_problem_dilemma",
        "title_es": "El Gran Dilema: Láser Diodo y Cámara en LightBurn",
        "title_en": "The Laser Workshop Dilemma: Diode Laser + Camera",
        "subtitle_es": "Peligros de los cables largos y el muro de pago de VirtualHere",
        "subtitle_en": "Hazards of long USB cables and VirtualHere paywalls",
        "audio_es": (
            "Si tienes una grabadora láser de diodo como Sculpfun, Atomstack, xTool, Ortur o Creality y usas LightBurn, "
            "seguro que sufres dos grandes problemas. El primero es tirar cables USB largos por el taller, que provocan ruido electromagnético "
            "y desconexiones a mitad de trabajo arruinando piezas de madera o metacrilato. El segundo es VirtualHere, cuya versión gratuita "
            "solo permite un único dispositivo, obligándote a pagar cuarenta y nueve dólares por máquina si quieres conectar el láser y la cámara a la vez. "
            "Con SnakeUSBIP conectas ambos simultáneamente y de forma totalmente gratuita."
        ),
        "audio_en": (
            "If you operate a diode laser engraver like Sculpfun, Atomstack, xTool, Ortur, or Creality and use LightBurn, "
            "you face two major headaches. First, running long USB cables across your workshop causes signal degradation, "
            "electromagnetic noise, and sudden disconnects that ruin expensive workpieces. Second, VirtualHere's free tier "
            "only allows a single device, forcing you to pay forty-nine dollars per machine just to connect your laser and camera at the same time. "
            "SnakeUSBIP solves this completely by connecting both simultaneously with zero licensing fees."
        ),
        "visual_type": "cards_comparison_laser"
    },
    {
        "id": "scene02_hardware_architecture",
        "title_es": "Arquitectura Hardware: SBC al Lado del Láser",
        "title_en": "Hardware Architecture: SBC Beside Your Laser",
        "subtitle_es": "Raspberry Pi, Orange Pi o Mini PC con doble conexión USB",
        "subtitle_en": "Raspberry Pi, Orange Pi, or Mini PC with dual USB links",
        "audio_es": (
            "El montaje en el taller es limpio y seguro. Colocamos un microordenador económico, como una Raspberry Pi, Orange Pi o mini PC con Linux, "
            "justo al lado del chasis del láser. En el puerto USB uno conectamos el controlador del láser, típicamente con chip CH340 o CP2102. "
            "En el puerto USB dos conectamos la cámara de alineación cenital de LightBurn. "
            "A partir de aquí, cero cables por el suelo: todos los datos viajarán por tu red Wi-Fi o cable Ethernet."
        ),
        "audio_en": (
            "The physical setup in your workshop is tidy and reliable. Place a budget-friendly single-board computer, like a Raspberry Pi, Orange Pi, "
            "or Linux mini-PC, right next to your laser enclosure. Into USB port one, plug your laser controller, typically running a CH340 or CP2102 chip. "
            "Into USB port two, plug your LightBurn overhead alignment camera. "
            "From this point onward, no cables snake across the floor: all communications travel securely over Wi-Fi or Ethernet."
        ),
        "visual_type": "architecture_diagram"
    },
    {
        "id": "scene03_server_setup",
        "title_es": "Instalación del Servidor en 1 Clic con udev Inteligente",
        "title_en": "1-Click Server Setup with Smart udev Hotplug",
        "subtitle_es": "Auto-exportación Plug & Play inmediata para tu láser y tu cámara",
        "subtitle_en": "Automatic Plug & Play export for your laser and camera",
        "audio_es": (
            "Configurar el servidor en la Raspberry Pi toma menos de un minuto. Conéctate por SSH y ejecuta nuestro comando oficial de una sola línea. "
            "El instalador descarga los módulos USB/IP del kernel, levanta el demonio del sistema y configura reglas inteligentes en udev. "
            "Gracias a esto, en cuanto enciendes el láser y la cámara, ambos puertos se comparten al instante en tu red de forma totalmente automática, "
            "sin tener que escribir comandos manuales de enlace."
        ),
        "audio_en": (
            "Configuring the server on your Raspberry Pi takes less than a minute. Connect over SSH and run our official one-line command. "
            "The installer downloads the USB/IP kernel packages, activates the system daemon, and deploys intelligent udev rules. "
            "As a result, the moment you power on your laser and camera, both devices are instantly shared over your network automatically, "
            "with zero manual binding commands required."
        ),
        "visual_type": "terminal_script"
    },
    {
        "id": "scene04_windows_whql",
        "title_es": "Instalación en Windows y Drivers WHQL de Microsoft",
        "title_en": "Windows Client & Microsoft WHQL Drivers",
        "subtitle_es": "Soporte oficial para Windows 10 y 11 con Integridad de Memoria (HVCI)",
        "subtitle_en": "Certified drivers for Windows 10 & 11 with Core Isolation (HVCI)",
        "audio_es": (
            "En el ordenador de diseño donde tienes LightBurn, descarga el instalador oficial de SnakeUSBIP. "
            "Incluye controladores virtuales certificados oficialmente por Microsoft mediante firma WHQL. "
            "Esto garantiza compatibilidad total con Windows 10 y Windows 11, funcionando a la perfección con Aislamiento de Núcleo e Integridad de Memoria activados, "
            "tanto en procesadores Intel y AMD de 64 bits como en equipos modernos ARM64."
        ),
        "audio_en": (
            "On your design computer running LightBurn, download the official SnakeUSBIP installer. "
            "It packages virtual bus drivers certified directly by Microsoft through official WHQL attestation. "
            "This guarantees seamless compatibility on Windows 10 and Windows 11, working out of the box with Core Isolation and Memory Integrity enabled, "
            "supporting both 64-bit Intel/AMD processors and modern ARM64 laptops."
        ),
        "visual_type": "whql_drivers"
    },
    {
        "id": "scene05_connect_both",
        "title_es": "Conexión Simultánea de Láser + Cámara y Favoritos",
        "title_en": "Simultaneous Laser + Camera Connection & Auto-Reconnect",
        "subtitle_es": "Un puerto COM virtual para el láser y un dispositivo UVC para la cámara",
        "subtitle_en": "Virtual COM port for the laser and native UVC for the camera",
        "audio_es": (
            "Al abrir SnakeUSBIP, su motor de escaneo localiza tu Raspberry Pi en segundos y muestra el ping en milisegundos en tiempo real. "
            "En la lista verás aparecer el controlador serie de tu láser y tu cámara web. Haz clic en Conectar en ambos. "
            "Windows creará un puerto COM virtual para el láser y un dispositivo de vídeo estándar para la cámara. "
            "Marca la casilla de Auto-conectar en ambos dispositivos para que se reconecten solos al encender el láser o reiniciar el equipo."
        ),
        "audio_en": (
            "When you launch SnakeUSBIP, its broadcast engine discovers your Raspberry Pi in seconds, showing live ping latency in milliseconds. "
            "You will see your laser's serial controller and your webcam listed. Click Connect on both. "
            "Windows creates a virtual COM port for the laser and a standard UVC video device for the camera. "
            "Check the Auto-connect box on both peripherals so they automatically re-attach whenever the laser is powered on or rebooted."
        ),
        "visual_type": "device_connect"
    },
    {
        "id": "scene06_performance_modes",
        "title_es": "Perfiles de Rendimiento: WSK para Láser y Zero-Copy para Cámara",
        "title_en": "Performance Profiles: WSK for Laser & Zero-Copy for Camera",
        "subtitle_es": "Cero retardo en jogging y encuadre, y máxima fluidez en vídeo",
        "subtitle_en": "Zero jitter on jogging/framing, and maximum video throughput",
        "audio_es": (
            "En la barra de estado inferior puedes alternar los perfiles de red. "
            "Para el controlador del láser, el modo Low-Latency WSK utiliza callbacks directos en el kernel para eliminar el jitter en el streaming de código G, "
            "logrando que el movimiento manual y el encuadre en LightBurn respondan al instante. "
            "Para la cámara de LightBurn, el modo Zero-Copy proporciona el máximo ancho de banda para ver la imagen en alta resolución de forma fluida y sin parpadeos."
        ),
        "audio_en": (
            "From the bottom status bar, you can switch network engine modes on the fly. "
            "For your laser controller, Low-Latency WSK mode utilizes direct kernel callbacks to eliminate packet jitter during G-code streaming, "
            "making manual jogging and laser framing in LightBurn respond instantly. "
            "For your overhead camera, Zero-Copy mode provides maximum network throughput for high-resolution, stutter-free video feeds."
        ),
        "visual_type": "performance_laser"
    },
    {
        "id": "scene07_lightburn_setup",
        "title_es": "Configuración en LightBurn: Puerto Serie y Calibración de Cámara",
        "title_en": "LightBurn Setup: Serial COM Port & Camera Alignment",
        "subtitle_es": "Paso a paso: Selección de puerto, consola GRBL y ventana de cámara",
        "subtitle_en": "Step-by-step: Port selection, GRBL console, and camera calibration",
        "audio_es": (
            "Ahora abrimos LightBurn. En la ventana Dispositivos, seleccionamos GRBL con conexión serie y elegimos el puerto COM virtual creado por SnakeUSBIP. "
            "La consola responderá de inmediato confirmando la conexión con tu láser. "
            "A continuación, abre la ventana Control de Cámara, selecciona la cámara remota en el desplegable y realiza la calibración y alineación visual. "
            "Ya puedes colocar tus materiales en la cama de nido de abeja, encuadrar visualmente con precisión milimétrica y lanzar el grabado desde tu escritorio."
        ),
        "audio_en": (
            "Now open LightBurn. In the Devices window, choose GRBL via Serial and select the virtual COM port generated by SnakeUSBIP. "
            "The console will instantly reply, confirming communication with your laser. "
            "Next, open the Camera Control window, choose the remote USB camera from the dropdown list, and complete the lens calibration and visual alignment. "
            "You can now place wood or acrylic on your honeycomb bed, align artwork with millimeter precision, and start engraving right from your desk."
        ),
        "visual_type": "lightburn_walkthrough"
    },
    {
        "id": "scene08_remote_vpn",
        "title_es": "Taller Remoto Seguro con VPN (Tailscale y WireGuard)",
        "title_en": "Secure Remote Workshop via VPN (Tailscale & WireGuard)",
        "subtitle_es": "Controla tu láser en el garaje o caseta de jardín sin abrir puertos",
        "subtitle_en": "Control your laser in a shed or garage without opening ports",
        "audio_es": (
            "Si tu cortadora láser está en un garaje separado, una caseta en el jardín o un taller en otra ubicación, "
            "no necesitas tocar el cortafuegos ni abrir puertos peligrosos en tu router. "
            "SnakeUSBIP se integra de forma nativa con redes malladas seguras como Tailscale, ZeroTier y WireGuard. "
            "Solo tienes que pulsar Añadir Servidor, introducir la IP de Tailscale de tu Raspberry Pi y podrás operar y supervisar por cámara tu láser "
            "desde el salón de tu casa o desde otra oficina con total comodidad y seguridad."
        ),
        "audio_en": (
            "If your laser engraver sits in a detached garage, backyard shed, or remote workshop, "
            "you never need to mess with router firewall rules or expose vulnerable ports to the internet. "
            "SnakeUSBIP features native compatibility with encrypted mesh VPNs like Tailscale, ZeroTier, and WireGuard. "
            "Simply click Add Server, enter your Raspberry Pi's Tailscale IP address, and you can control and visually monitor your laser "
            "from the comfort of your living room or remote office with complete security."
        ),
        "visual_type": "vpn_remote"
    },
    {
        "id": "scene09_summary_cta",
        "title_es": "La Solución Definitiva para Makers: 100% Gratuita",
        "title_en": "The Ultimate Free Tool for Laser Makers: Download Now",
        "subtitle_es": "Sin licencias de 49$, sin cortes de cable y con soporte multidisciplinar",
        "subtitle_en": "No $49 licenses, no cable disconnects, and full maker freedom",
        "audio_es": (
            "En conclusión: conexión simultánea e ilimitada de tu láser diodo y tu cámara en LightBurn, "
            "cero desconexiones por cables largos, auto-reconexión tolerante a fallos, baja latencia para un encuadre milimétrico y control seguro por VPN. "
            "Todo ello sin pagar licencias de cuarenta y nueve dólares y con controladores certificados de máxima estabilidad. "
            "Descarga ya SnakeUSBIP desde nuestro repositorio oficial en GitHub, apoya el proyecto con una estrella y disfruta de la libertad de tu taller láser."
        ),
        "audio_en": (
            "In conclusion: simultaneous and unlimited connection of your diode laser and camera in LightBurn, "
            "zero mid-burn disconnects from long cables, fault-tolerant auto-reconnect, low latency for pinpoint framing, and secure VPN routing. "
            "All of this without paying forty-nine dollar per-device licenses and with officially certified drivers. "
            "Download SnakeUSBIP today from our official GitHub repository, support the project with a star, and enjoy complete freedom in your laser workshop."
        ),
        "visual_type": "summary_cta"
    }
]

def generate_audio_elevenlabs(scene, lang, voice_id, api_key):
    scene_id = scene["id"]
    text = scene[f"audio_{lang}"]
    out_path = os.path.join(TEMP_DIR, f"{scene_id}_{lang}.mp3")

    # Strict Zero-Waste Cache check
    if os.path.exists(out_path) and os.path.getsize(out_path) > 2000:
        print(f"  [CACHE HIT] {scene_id}_{lang} already exists ({os.path.getsize(out_path)} bytes). 0 API credits spent.")
        return out_path

    print(f"  [SYNTHESIZING] {scene_id} ({len(text)} chars | {lang.upper()}) with voice 'oscar asturias' [Turbo 2.5 Expressive]...")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = {
        "text": text,
        "model_id": "eleven_turbo_v2_5",
        "language_code": lang,
        "voice_settings": {
            "stability": 0.33,
            "similarity_boost": 0.75,
            "style": 0.45,
            "use_speaker_boost": True,
            "speed": 1.02
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
    try:
        with urllib.request.urlopen(req) as resp:
            audio_bytes = resp.read()
            with open(out_path, "wb") as f:
                f.write(audio_bytes)
        print(f"  [SAVED] {out_path} ({len(audio_bytes)} bytes)")
        return out_path
    except Exception as ex:
        print(f"  [WARNING] ElevenLabs API error: {ex}. Falling back to Windows SAPI TTS...")
        return fallback_tts(text, out_path)

def fallback_tts(text, out_path):
    ps_script = f"""
    Add-Type -AssemblyName System.Speech;
    $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer;
    $synth.SetOutputToWaveFile('{out_path}.wav');
    $synth.Speak(@'
{text}
'@);
    $synth.Dispose();
    """
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], check=True)
    subprocess.run(["ffmpeg", "-y", "-i", f"{out_path}.wav", "-codec:a", "libmp3lame", "-qscale:a", "2", out_path], check=True)
    if os.path.exists(f"{out_path}.wav"):
        os.remove(f"{out_path}.wav")
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
    im = Image.new("RGB", (w, h), color="#090D16")
    draw = ImageDraw.Draw(im)

    # Accent Top Header Bar (Cyan to Laser Amber accent)
    draw.rectangle([(0, 0), (w, 12)], fill="#F59E0B")

    # Header Brand
    draw.text((80, 45), "⚡ SnakeUSBIP", font=get_font(FONT_BOLD, 32), fill="#06B6D4")
    badge_text = "   Laser & LightBurn Masterclass     v3.0.0" if lang == "en" else "   Masterclass Láser & LightBurn     v3.0.0"
    draw.text((360, 52), badge_text, font=get_font(FONT_BOLD, 22), fill="#94A3B8")

    # Title & Subtitle
    draw.text((80, 115), scene[f"title_{lang}"], font=get_font(FONT_BOLD, 48), fill="#F8FAFC")
    draw.text((80, 182), scene[f"subtitle_{lang}"], font=get_font(FONT_REGULAR, 26), fill="#FBBF24")

    vtype = scene["visual_type"]

    if vtype == "cards_comparison_laser":
        # Card 1: VirtualHere & Long Cables
        draw.rounded_rectangle([(80, 260), (920, 940)], radius=20, fill="#1E1B24", outline="#DC2626", width=2)
        draw.text((120, 300), "❌ The Old Way (VirtualHere)", font=get_font(FONT_BOLD, 34), fill="#EF4444")
        pts1 = [
            "  Strict 1-Device Limit on Free tier",
            "  Cannot connect Laser + Camera together",
            "  $49.00 USD / server license locked to hardware",
            "  5-meter USB cable drops mid-burn (ruined acrylic)",
            "  Electromagnetic interference from stepper motors",
            "  Restarting LightBurn required after power cycles"
        ] if lang == "en" else [
            "  Límite estricto de 1 solo dispositivo en versión Free",
            "  Imposible conectar Láser + Cámara a la vez gratis",
            "  Licencia de 49,00 $ atada a la placa de por vida",
            "  Cables USB largos que se desconectan y rompen piezas",
            "  Ruido e interferencias parásitas de los motores paso a paso",
            "  Obliga a reiniciar LightBurn si el láser se apaga"
        ]
        y = 380
        for p in pts1:
            draw.text((120, y), p, font=get_font(FONT_REGULAR, 24), fill="#E2E8F0")
            y += 75

        # Card 2: SnakeUSBIP Solution
        draw.rounded_rectangle([(1000, 260), (1840, 940)], radius=20, fill="#0F2D37", outline="#10B981", width=3)
        draw.text((1040, 300), "✅ The SnakeUSBIP Solution", font=get_font(FONT_BOLD, 34), fill="#10B981")
        pts2 = [
            "  100% Free & Unlimited Simultaneous Devices",
            "  Laser Controller (CH340/CP2102) + 4K Camera together",
            "  Zero cables across workshop: Wi-Fi or Ethernet",
            "  Fault-tolerant Auto-Reconnect on power resets",
            "  Low-Latency WSK mode for real-time framing & jogging",
            "  Native VPN (Tailscale/WireGuard) for remote sheds"
        ] if lang == "en" else [
            "  100% Gratuito y Dispositivos Simultáneos Ilimitados",
            "  Controlador Láser + Cámara Cenital juntos a la vez",
            "  Cero cables cruzando el taller: todo por Wi-Fi o Ethernet",
            "  Auto-reconexión inmediata si apagas o reseteas el láser",
            "  Modo WSK de ultrabaja latencia para encuadre en vivo",
            "  VPN nativa (Tailscale/WireGuard) para garajes remotos"
        ]
        y = 380
        for p in pts2:
            draw.text((1040, y), p, font=get_font(FONT_REGULAR, 24), fill="#F8FAFC")
            y += 75

    elif vtype == "architecture_diagram":
        # Workshop Architecture Box
        draw.rounded_rectangle([(80, 260), (1840, 940)], radius=20, fill="#131D31", outline="#38BDF8", width=2)
        draw.text((120, 295), "📐 WORKSHOP PHYSICAL TOPOLOGY", font=get_font(FONT_BOLD, 30), fill="#38BDF8")
        
        # Laser Machine Box
        draw.rounded_rectangle([(120, 370), (580, 890)], radius=16, fill="#1E293B", outline="#F59E0B", width=2)
        draw.text((150, 400), "🔥 Diode Laser Machine", font=get_font(FONT_BOLD, 26), fill="#F59E0B")
        l_info = [
            "  Sculpfun, Atomstack, xTool,",
            "  Ortur, Creality, TwoTrees, etc.",
            "",
            "  🔌 USB Port 1: GRBL Board",
            "     (CH340 / CP2102 / FTDI)",
            "",
            "  📷 USB Port 2: Alignment Cam",
            "     (5MP / 8MP / 4K LightBurn Cam)"
        ] if lang == "en" else [
            "  Sculpfun, Atomstack, xTool,",
            "  Ortur, Creality, TwoTrees, etc.",
            "",
            "  🔌 Puerto USB 1: Placa GRBL",
            "     (CH340 / CP2102 / FTDI)",
            "",
            "  📷 Puerto USB 2: Cámara Cenital",
            "     (Cámara 5MP/8MP/4K LightBurn)"
        ]
        y = 470
        for l in l_info:
            draw.text((150, y), l, font=get_font(FONT_REGULAR, 22), fill="#E2E8F0")
            y += 45

        # Arrow 1
        draw.text((630, 600), "Short USB\nCables (0.5m)\n========>", font=get_font(FONT_BOLD, 22), fill="#10B981")

        # Raspberry Pi Box
        draw.rounded_rectangle([(800, 370), (1240, 890)], radius=16, fill="#1E293B", outline="#06B6D4", width=2)
        draw.text((830, 400), "🍓 SBC Server (Next to Laser)", font=get_font(FONT_BOLD, 26), fill="#06B6D4")
        sbc_info = [
            "  Raspberry Pi 3B / 4 / 5,",
            "  Orange Pi, Armbian, or Mini PC",
            "",
            "  ⚡ SnakeUSBIP Server Daemon",
            "  ⚡ Smart udev Hotplug rules",
            "  ⚡ Auto-shares both USB ports",
            "  ⚡ Low-power (5W), runs 24/7"
        ] if lang == "en" else [
            "  Raspberry Pi 3B / 4 / 5,",
            "  Orange Pi, Armbian o Mini PC",
            "",
            "  ⚡ Demonio SnakeUSBIP Server",
            "  ⚡ Reglas udev inteligentes",
            "  ⚡ Exporta ambos puertos solos",
            "  ⚡ Bajo consumo (5W), 24/7"
        ]
        y = 470
        for s in sbc_info:
            draw.text((830, y), s, font=get_font(FONT_REGULAR, 22), fill="#E2E8F0")
            y += 45

        # Arrow 2
        draw.text((1280, 600), "Wi-Fi / LAN\nor VPN\n========>", font=get_font(FONT_BOLD, 22), fill="#38BDF8")

        # Design PC Box
        draw.rounded_rectangle([(1430, 370), (1800, 890)], radius=16, fill="#1E293B", outline="#10B981", width=2)
        draw.text((1450, 400), "💻 Windows PC", font=get_font(FONT_BOLD, 26), fill="#10B981")
        pc_info = [
            "  Your Desk / House",
            "",
            "  🔥 LightBurn / LaserGRBL",
            "  🌐 SnakeUSBIP Client",
            "",
            "  ✅ Virtual COM3 (Laser)",
            "  ✅ Virtual UVC (Camera)"
        ] if lang == "en" else [
            "  Tu Escritorio / Casa",
            "",
            "  🔥 LightBurn / LaserGRBL",
            "  🌐 Cliente SnakeUSBIP",
            "",
            "  ✅ Puerto COM3 (Láser)",
            "  ✅ Dispositivo UVC (Cámara)"
        ]
        y = 470
        for p in pc_info:
            draw.text((1450, y), p, font=get_font(FONT_REGULAR, 22), fill="#F8FAFC")
            y += 45

    elif vtype == "terminal_script":
        # Terminal visual
        draw.rounded_rectangle([(80, 260), (1840, 940)], radius=20, fill="#030712", outline="#334155", width=2)
        draw.ellipse([(110, 285), (130, 305)], fill="#EF4444")
        draw.ellipse([(145, 285), (165, 305)], fill="#F59E0B")
        draw.ellipse([(180, 285), (200, 305)], fill="#10B981")
        draw.text((220, 284), "bash: raspberrypi@laser-workshop ~ (One-Line Automated Setup)", font=get_font(FONT_REGULAR, 20), fill="#64748B")

        draw.text((120, 345), "$ curl -sSL https://raw.githubusercontent.com/oscarlosu-lab/SnakeUSBIP/main/scripts/install-server.sh | sudo bash", font=get_font(FONT_CODE, 23), fill="#38BDF8")
        lines = [
            "[*] Step 1/4: Installing USB/IP kernel packages (usbip, hwdata, usbutils)... [DONE]",
            "[*] Step 2/4: Loading kernel drivers in /etc/modules-load.d/usbip.conf... [DONE]",
            "[*] Step 3/4: Installing Plug & Play Auto-Bind engine to /usr/local/bin/snakeusbip-autobind.sh...",
            "[*] Step 4/4: Enabling systemd background daemon (snakeusbip.service) and udev rules...",
            "",
            "[+] SUCCESS: SnakeUSBIP Server is now active on TCP port 3240!",
            "[+] HOTPLUG ACTIVE: Plug your CH340 Laser & USB Camera in any port: they auto-export instantly!"
        ] if lang == "en" else [
            "[*] Paso 1/4: Instalando paquetes USB/IP del kernel (usbip, hwdata, usbutils)... [OK]",
            "[*] Paso 2/4: Cargando controladores en /etc/modules-load.d/usbip.conf... [OK]",
            "[*] Paso 3/4: Instalando motor de Auto-Bind Plug & Play en /usr/local/bin/snakeusbip-autobind.sh...",
            "[*] Paso 4/4: Activando demonio del sistema (snakeusbip.service) y reglas de udev...",
            "",
            "[+] ÉXITO: ¡Servidor SnakeUSBIP activo y escuchando en el puerto TCP 3240!",
            "[+] HOTPLUG ACTIVO: Conecta tu láser CH340 y tu cámara: ¡se comparten solos al instante!"
        ]
        y = 425
        for l in lines:
            col = "#10B981" if "[+]" in l or "[DONE]" in l or "[OK]" in l else "#94A3B8"
            draw.text((120, y), l, font=get_font(FONT_CODE, 22), fill=col)
            y += 55

        draw.rounded_rectangle([(120, 780), (1800, 900)], radius=12, fill="#1E293B", outline="#0EA5E9", width=2)
        tip_text = "💡 Zero Maintenance: No manual CLI commands needed ever again. Plug, unplug, or power cycle freely." if lang == "en" else "💡 Cero Mantenimiento: Jamás tendrás que escribir comandos de enlace. Enciende y apaga el láser con total libertad."
        draw.text((150, 825), tip_text, font=get_font(FONT_BOLD, 22), fill="#FBBF24")

    else:
        # Side-by-side Layout with UI screenshot and points
        cap_file = None
        if vtype == "whql_drivers":
            cap_file = os.path.join(ASSETS_DIR, "app_frame.png")
        elif vtype in ("device_connect", "performance_laser"):
            cap_file = os.path.join(CAPTURES_DIR, "capture_01_mainwindow_dark.png")
        elif vtype == "vpn_remote":
            cap_file = os.path.join(CAPTURES_DIR, "capture_03_vpn_dialog.png")
        else:
            cap_file = os.path.join(CAPTURES_DIR, "capture_04_mainwindow_light.png")

        if cap_file and os.path.exists(cap_file):
            try:
                cap_im = Image.open(cap_file)
                cap_im.thumbnail((840, 640), Image.Resampling.LANCZOS)
                im.paste(cap_im, (80, 260))
            except Exception:
                pass
        else:
            draw.rounded_rectangle([(80, 260), (920, 940)], radius=20, fill="#1E293B", outline="#334155", width=2)
            draw.text((120, 310), "🖥️ SnakeUSBIP UI", font=get_font(FONT_BOLD, 32), fill="#38BDF8")

        # Right Panel
        draw.rounded_rectangle([(960, 260), (1840, 940)], radius=20, fill="#131D31", outline="#0284C7", width=2)
        font_h = get_font(FONT_BOLD, 30)
        font_b = get_font(FONT_REGULAR, 23)

        if vtype == "whql_drivers":
            h_text = "🛡️ Certified WHQL Driver Security" if lang == "en" else "🛡️ Drivers WHQL Certificados por Microsoft"
            pts = [
                "  Official Microsoft Hardware Compatibility Publisher stamp",
                "  100% compatible with Core Isolation / Memory Integrity (HVCI)",
                "  Zero test-signing mode or disabled Secure Boot required",
                "  Clean two-stage PnP installation via Inno Setup",
                "  Stops duplicate virtual controllers in Device Manager",
                "  Supports Windows 10 & 11 (x64 and ARM64 architecture)"
            ] if lang == "en" else [
                "  Sello oficial de Microsoft Windows Hardware Compatibility",
                "  100% compatible con Aislamiento de Núcleo e Integridad (HVCI)",
                "  Cero modo de pruebas y sin desactivar Secure Boot",
                "  Instalación limpia PnP en dos etapas vía Inno Setup",
                "  Previene controladores virtuales duplicados en el Administrador",
                "  Soporta Windows 10 y 11 (arquitecturas x64 y ARM64)"
            ]
        elif vtype == "device_connect":
            h_text = "🔌 Dual Device Link (Laser + Cam)" if lang == "en" else "🔌 Doble Enlace (Láser + Cámara)"
            pts = [
                "  Auto-detects Raspberry Pi with live latency (e.g. 0.8 ms)",
                "  Device 1: CH340 / CP2102 GRBL Laser Controller -> Click Connect",
                "     -> Windows instantly registers a Virtual COM port (COM3)",
                "  Device 2: HD LightBurn Alignment Webcam -> Click Connect",
                "     -> Windows binds a native UVC Imaging Device",
                "  ⭐ Check 'Auto-connect' on both for startup favorites",
                "  Instant reconnect if the laser is turned off and on again"
            ] if lang == "en" else [
                "  Detecta la Raspberry Pi con medidor de ping en vivo (0.8 ms)",
                "  Dispositivo 1: Placa GRBL Láser (CH340/CP2102) -> Pulsa Conectar",
                "     -> Windows crea un puerto COM virtual de inmediato (COM3)",
                "  Dispositivo 2: Cámara Cenital LightBurn -> Pulsa Conectar",
                "     -> Windows monta un dispositivo de imagen UVC nativo",
                "  ⭐ Marca la casilla 'Auto-conectar' para favoritos de inicio",
                "  Reconexión instantánea ante cortes de luz o apagado del láser"
            ]
        elif vtype == "performance_laser":
            h_text = "⚡ Tailored Performance Engines" if lang == "en" else "⚡ Motores de Red Especializados"
            pts = [
                "🎯 LOW-LATENCY WSK ENGINE (For the Laser):",
                "     Direct Winsock Kernel event callbacks",
                "     Zero command buffering and no packet jitter",
                "     Real-time jogging and razor-sharp laser framing",
                "📷 ZERO-COPY ENGINE (For the Camera):",
                "     Maximum continuous network throughput",
                "     Uncompressed / MJPEG video streams without drops",
                "     Ideal for 1080p and 4K LightBurn overhead lenses"
            ] if lang == "en" else [
                "🎯 MODO LOW-LATENCY WSK (Para el Láser):",
                "     Callbacks asíncronos en el kernel de Windows",
                "     Cero búferes intermedios y sin retardo de paquetes",
                "     Respuesta inmediata al mover los ejes y en el encuadre",
                "📷 MODO ZERO-COPY (Para la Cámara):",
                "     Máximo ancho de banda de red continuo",
                "     Transmisión de vídeo MJPEG sin caídas de frames",
                "     Ideal para cámaras cenitales 1080p y 4K en LightBurn"
            ]
        elif vtype == "lightburn_walkthrough":
            h_text = "🔥 LightBurn Step-by-Step Setup" if lang == "en" else "🔥 Configuración Paso a Paso en LightBurn"
            pts = [
                "  1. Devices -> Find My Laser or Manual -> GRBL (Serial)",
                "  2. Choose the SnakeUSBIP Virtual COM Port (115200 Baud)",
                "  3. Console confirms: 'Grbl 1.1h ['$' for help] ok'",
                "  4. Window -> Camera Control -> Select SnakeUSBIP Webcam",
                "  5. Run 'Calibrate Camera Lens' & 'Calibrate Camera Alignment'",
                "  6. Visually place your graphic over raw wood & press Start!",
                "  7. Zero computer noise and zero toxic smoke at your desk"
            ] if lang == "en" else [
                "  1. Dispositivos -> Crear manual -> GRBL (Serial/USB)",
                "  2. Elige el puerto COM virtual de SnakeUSBIP (115200 Baudios)",
                "  3. La consola responde: 'Grbl 1.1h ['$' for help] ok'",
                "  4. Ventana -> Control de Cámara -> Selecciona la webcam remota",
                "  5. Ejecuta 'Calibrar Lente de Cámara' y 'Calibrar Alineación'",
                "  6. ¡Coloca tu diseño sobre la madera en pantalla y graba!",
                "  7. Cero humos tóxicos y cero ruido en tu escritorio"
            ]
        elif vtype == "vpn_remote":
            h_text = "🌐 Remote Workshop (Tailscale / VPN)" if lang == "en" else "🌐 Taller Remoto Seguro (Tailscale / VPN)"
            pts = [
                "  Laser in a backyard shed, detached garage, or makerspace?",
                "  Install Tailscale or WireGuard on the Raspberry Pi and PC",
                "  Click 'Add Server' in SnakeUSBIP -> Enter 100.x.x.x VPN IP",
                "  Full encrypted peer-to-peer tunnel: zero router ports opened",
                "  Supervise the live camera stream from your living room",
                "  Pause or cancel jobs instantly if you see flare-ups",
                "  Works over Wi-Fi, Ethernet, 4G/5G, and across town"
            ] if lang == "en" else [
                "  ¿Láser en un garaje separado, caseta exterior o makerspace?",
                "  Instala Tailscale o WireGuard en la Raspberry Pi y en tu PC",
                "  Pulsa 'Añadir Servidor' en SnakeUSBIP -> Pon la IP VPN (100.x.x.x)",
                "  Túnel cifrado punto a punto: cero puertos abiertos en el router",
                "  Supervisa el vídeo en vivo de la cámara desde el salón",
                "  Pausa o detén el trabajo al instante si detectas anomalías",
                "  Funciona por Wi-Fi, cable, 4G/5G y entre distintas ubicaciones"
            ]
        elif vtype == "summary_cta":
            h_text = "🚀 Masterclass Takeaways & Download" if lang == "en" else "🚀 Resumen y Enlaces de Descarga"
            pts = [
                "  ✅ Simultaneous Diode Laser + Camera (Unlimited Devices)",
                "  ✅ 100% Free & Open Source: Say goodbye to $49 licenses",
                "  ✅ No dangerous cables: Wi-Fi, LAN, or Tailscale VPN",
                "  ✅ WHQL Certified Windows 10/11 drivers (HVCI ready)",
                "  ✅ Instant Auto-Reconnect on power resets",
                "  📦 Download latest v3.0.0 from GitHub Releases:",
                "     👉 github.com/oscarlosu-lab/SnakeUSBIP",
                "  ⭐ Support the project with a Star on GitHub!"
            ] if lang == "en" else [
                "  ✅ Láser Diodo + Cámara simultáneos (Dispositivos Ilimitados)",
                "  ✅ 100% Libre y Gratuito: Adiós a las licencias de 49$",
                "  ✅ Cero cables peligrosos: Vía Wi-Fi, Ethernet o Tailscale VPN",
                "  ✅ Drivers certificados WHQL en Windows 10/11 (HVCI ready)",
                "  ✅ Auto-reconexión instantánea ante cortes de luz",
                "  📦 Descarga la última versión v3.0.0 en GitHub Releases:",
                "     👉 github.com/oscarlosu-lab/SnakeUSBIP",
                "  ⭐ ¡Apoya el proyecto dejando tu estrella en GitHub!"
            ]

        draw.text((1000, 295), h_text, font=font_h, fill="#38BDF8")
        y = 380
        for pt in pts:
            col = "#F8FAFC" if not pt.startswith("🎯") and not pt.startswith("📷") and not pt.startswith("👉") and not pt.startswith("⭐") else ("#F59E0B" if "WSK" in pt or "Láser" in pt or "Laser" in pt else "#10B981")
            draw.text((1000, y), pt, font=font_b, fill=col)
            y += 58

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

def build_laser_video(lang="es"):
    api_key, voice_id = get_elevenlabs_credentials()
    if not api_key:
        print("[!] Warning: No ElevenLabs API key found. Will use local Windows SAPI fallback.")

    print("╔═════════════════════════════════════════════════════════════════════════════╗")
    print(f"║ 🎥 SnakeUSBIP Laser & LightBurn Video Generator [{lang.upper()}]                ║")
    print(f"║ 🎙️ Narration: oscar asturias via Multilingual v2 / Zero-Waste Disk Caching  ║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝\n")

    total_chars = sum(len(s[f"audio_{lang}"]) for s in SCENES)
    print(f"[*] Total scenes: {len(SCENES)}")
    print(f"[*] Total narration characters: {total_chars:,} characters\n")

    scene_clips = []
    scene_durations = []

    for idx, scene in enumerate(SCENES, 1):
        sid = scene["id"]
        print(f"[{idx}/{len(SCENES)}] Processing scene: {sid} [{lang.upper()}]...")

        # 1. Audio
        audio_file = generate_audio_elevenlabs(scene, lang, voice_id, api_key)
        duration = get_audio_duration(audio_file)
        padded_duration = duration + 0.6
        scene_durations.append((scene, padded_duration))
        print(f"      Audio duration: {duration:.2f}s (Padded Clip: {padded_duration:.2f}s)")

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
    srt_output = os.path.join(OUTPUT_DIR, f"SnakeUSBIP_Laser_LightBurn_Tutorial_{lang.upper()}.srt")
    generate_srt(scene_durations, srt_output, lang)
    print(f"\n[✓] Subtitles generated: {srt_output}")

    # 5. Concatenate
    concat_list = os.path.join(TEMP_DIR, f"concat_list_{lang}.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        for c in scene_clips:
            clean_path = c.replace("\\", "/")
            f.write(f"file '{clean_path}'\n")

    final_video = os.path.join(OUTPUT_DIR, f"SnakeUSBIP_Laser_LightBurn_Tutorial_{lang.upper()}.mp4")
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

    print(f"\n[🎉 SUCCESS] 1080p Tutorial Video Generated: {final_video}")
    print(f"             Synchronized Subtitles: {srt_output}\n")

if __name__ == "__main__":
    lang = "es"
    if "--lang" in sys.argv:
        idx = sys.argv.index("--lang")
        if idx + 1 < len(sys.argv):
            lang = sys.argv[idx + 1].lower()
    
    if "--all" in sys.argv:
        build_laser_video("es")
        build_laser_video("en")
    else:
        build_laser_video(lang)
