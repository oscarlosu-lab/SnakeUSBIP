#!/usr/bin/env python3
"""Generates 1280x720 (16:9) YouTube Thumbnails for SnakeUSBIP Laser & LightBurn Tutorial (ES & EN)"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(REPO_ROOT, "docs", "assets")
RELEASE_DIR = os.path.join(REPO_ROOT, "release")

FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_REGULAR = r"C:\Windows\Fonts\segoeui.ttf"
FONT_BLACK = r"C:\Windows\Fonts\arialbd.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def create_laser_thumbnail(lang="es", out_path="thumbnail.png"):
    w, h = 1280, 720
    im = Image.new("RGB", (w, h), color="#070A12")
    draw = ImageDraw.Draw(im)

    # Accent Top & Bottom Borders (Laser Amber / Fire gradient aesthetic)
    draw.rectangle([(0, 0), (w, 10)], fill="#F97316")
    draw.rectangle([(0, h - 10), (w, h)], fill="#06B6D4")

    # Main Card
    draw.rounded_rectangle([(30, 30), (1250, 690)], radius=24, fill="#0B132B", outline="#1E293B", width=2)

    # Fonts
    font_badge = get_font(FONT_BOLD, 22)
    font_hero = get_font(FONT_BLACK, 60)
    font_subhero = get_font(FONT_BOLD, 36)
    font_tag = get_font(FONT_BOLD, 25)

    # Badge 1: 100% Free
    badge_text = "🔥 100% GRATIS • SIN LÍMITE DE DISPOSITIVOS" if lang == "es" else "🔥 100% FREE • MULTI-DEVICE SUPPORT"
    draw.rounded_rectangle([(65, 65), (570, 115)], radius=12, fill="#064E3B", outline="#10B981", width=2)
    draw.text((85, 76), badge_text, font=font_badge, fill="#34D399")

    # Hero Title
    if lang == "es":
        draw.text((65, 140), "LÁSER DIODO", font=font_hero, fill="#F97316")
        draw.text((500, 140), "+ CÁMARA", font=font_hero, fill="#FFFFFF")
        draw.text((65, 218), "A LIGHTBURN SIN CABLES", font=font_subhero, fill="#38BDF8")
    else:
        draw.text((65, 140), "DIODE LASER", font=font_hero, fill="#F97316")
        draw.text((490, 140), "+ CAMERA", font=font_hero, fill="#FFFFFF")
        draw.text((65, 218), "TO LIGHTBURN WIRELESSLY", font=font_subhero, fill="#38BDF8")

    # VirtualHere Comparison Callout
    callout_box = [(65, 275), (660, 335)]
    draw.rounded_rectangle(callout_box, radius=12, fill="#7F1D1D", outline="#EF4444", width=2)
    callout_txt = "⚡ Adiós al Paywall de 49$ de VirtualHere" if lang == "es" else "⚡ Skip VirtualHere's $49 Device Paywall"
    draw.text((85, 290), callout_txt, font=get_font(FONT_BOLD, 24), fill="#FECACA")

    # Features Pill List
    features = [
        ("🎯 Cero Jitter WSK (G-Code Stream Perfecto)", "#F59E0B"),
        ("📷 Cámara Cenital UVC USB (Alineación HD)", "#06B6D4"),
        ("🌐 Taller Remoto con VPN (Tailscale / WireGuard)", "#10B981"),
        ("🛡️ Drivers Oficiales WHQL (Windows 10 / 11)", "#A855F7")
    ] if lang == "es" else [
        ("🎯 Zero Jitter WSK (Flawless G-Code Streaming)", "#F59E0B"),
        ("📷 Overhead UVC USB Camera (HD Alignment)", "#06B6D4"),
        ("🌐 Remote Workshop over VPN (Tailscale / WireGuard)", "#10B981"),
        ("🛡️ Official WHQL Certified Drivers (Win 10/11)", "#A855F7")
    ]

    y = 355
    for txt, col in features:
        draw.rounded_rectangle([(65, y), (660, y + 54)], radius=12, fill="#1E293B", outline=col, width=2)
        draw.text((85, y + 12), txt, font=font_tag, fill="#F8FAFC")
        y += 66

    # Bottom Pill: Full Tutorial
    tut_text = "TUTORIAL PASO A PASO 2026" if lang == "es" else "STEP-BY-STEP MASTERCLASS 2026"
    draw.rounded_rectangle([(65, 620), (660, 672)], radius=12, fill="#111827", outline="#38BDF8", width=2)
    draw.text((110, 632), tut_text, font=get_font(FONT_BOLD, 24), fill="#38BDF8")

    # Right Side: Visual Mockup / Connection Diagram Card
    rx, ry, rw, rh = 700, 70, 520, 595
    draw.rounded_rectangle([(rx, ry), (rx + rw, ry + rh)], radius=20, fill="#111C38", outline="#06B6D4", width=2)

    # Header inside right card
    draw.rounded_rectangle([(rx, ry), (rx + rw, ry + 60)], radius=20, fill="#1E293B")
    draw.text((rx + 30, ry + 16), "⚡ SnakeUSBIP Multi-PnP Engine", font=get_font(FONT_BOLD, 22), fill="#38BDF8")

    # Devices connected mockup
    # 1. Laser Card
    draw.rounded_rectangle([(rx + 25, ry + 85), (rx + rw - 25, ry + 225)], radius=14, fill="#16223F", outline="#F97316", width=2)
    draw.text((rx + 45, ry + 98), "🔥 DIODE LASER CONTROLLER", font=get_font(FONT_BOLD, 21), fill="#F97316")
    draw.text((rx + 45, ry + 130), "• Chipset: CH340 / CP2102 (GRBL 1.1h)", font=get_font(FONT_REGULAR, 18), fill="#CBD5E1")
    draw.text((rx + 45, ry + 158), "• Engine: Low-Latency WSK (Zero Jitter)", font=get_font(FONT_BOLD, 18), fill="#10B981")
    draw.text((rx + 45, ry + 186), "• Windows Port: Virtual COM3 (Connected)", font=get_font(FONT_BOLD, 18), fill="#38BDF8")

    # 2. Camera Card
    draw.rounded_rectangle([(rx + 25, ry + 245), (rx + rw - 25, ry + 385)], radius=14, fill="#16223F", outline="#06B6D4", width=2)
    draw.text((rx + 45, ry + 258), "📷 OVERHEAD WORKSHOP CAMERA", font=get_font(FONT_BOLD, 21), fill="#06B6D4")
    draw.text((rx + 45, ry + 290), "• Sensor: 4K / 1080p UVC Video Device", font=get_font(FONT_REGULAR, 18), fill="#CBD5E1")
    draw.text((rx + 45, ry + 318), "• Engine: Zero-Copy Fast Frame Transfer", font=get_font(FONT_BOLD, 18), fill="#10B981")
    draw.text((rx + 45, ry + 346), "• LightBurn: Direct Lens Visual Alignment", font=get_font(FONT_BOLD, 18), fill="#FCD34D")

    # 3. Software Compatibility Badge
    draw.rounded_rectangle([(rx + 25, ry + 405), (rx + rw - 25, ry + 565)], radius=14, fill="#0F172A", outline="#10B981", width=2)
    draw.text((rx + 45, ry + 420), "COMPATIBILIDAD VERIFICADA" if lang == "es" else "VERIFIED COMPATIBILITY", font=get_font(FONT_BOLD, 20), fill="#10B981")
    apps = [
        "✔ LightBurn (v1.4, v1.5, v1.6+)",
        "✔ LaserGRBL (v5.x+)",
        "✔ Ruida / GRBL / Smoothieware",
        "✔ Raspberry Pi 3/4/5, Orange Pi, PC"
    ]
    ay = ry + 455
    for a in apps:
        draw.text((rx + 45, ay), a, font=get_font(FONT_REGULAR, 18), fill="#F1F5F9")
        ay += 26

    im.save(out_path, quality=95)
    print(f"[✓] Thumbnail saved: {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == "__main__":
    t_es = os.path.join(RELEASE_DIR, "youtube_laser_thumbnail_es.png")
    t_en = os.path.join(RELEASE_DIR, "youtube_laser_thumbnail_en.png")
    create_laser_thumbnail("es", t_es)
    create_laser_thumbnail("en", t_en)
