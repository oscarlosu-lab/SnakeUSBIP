#!/usr/bin/env python3
"""Generates 1280x720 (16:9) YouTube Thumbnails for SnakeUSBIP Masterclass (ES & EN)"""
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

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def create_thumbnail(lang="es", out_path="thumbnail.png"):
    w, h = 1280, 720
    im = Image.new("RGB", (w, h), color="#090D16")
    draw = ImageDraw.Draw(im)

    # Accent Top & Bottom Borders
    draw.rectangle([(0, 0), (w, 10)], fill="#06B6D4") # Cyan
    draw.rectangle([(0, h - 10), (w, h)], fill="#06B6D4")

    # Gradient-like background cards
    draw.rounded_rectangle([(40, 40), (1240, 680)], radius=24, fill="#0F172A", outline="#1E293B", width=2)

    # Left Side: Big Bold Punchy Headlines
    font_badge = get_font(FONT_BOLD, 22)
    font_hero = get_font(FONT_BOLD, 64)
    font_subhero = get_font(FONT_BOLD, 42)
    font_tag = get_font(FONT_BOLD, 26)

    # Badge: FREE & OPEN SOURCE
    badge_text = "🔥 100% GRATIS • OPEN SOURCE" if lang == "es" else "🔥 100% FREE • OPEN SOURCE"
    draw.rounded_rectangle([(80, 80), (520, 130)], radius=12, fill="#047857", outline="#10B981", width=2)
    draw.text((105, 92), badge_text, font=font_badge, fill="#ECFDF5")

    if lang == "es":
        draw.text((80, 160), "¡ADIÓS", font=font_hero, fill="#FFFFFF")
        draw.text((340, 160), "VIRTUALHERE!", font=font_hero, fill="#EF4444")
        draw.text((80, 245), "USB por Red Ilimitado", font=font_subhero, fill="#38BDF8")
    else:
        draw.text((80, 160), "FREE", font=font_hero, fill="#10B981")
        draw.text((260, 160), "VIRTUALHERE", font=font_hero, fill="#FFFFFF")
        draw.text((80, 245), "ALTERNATIVE", font=font_hero, fill="#EF4444")

    # Features Pill List
    features = [
        ("⚡ 0$ vs 49$ VirtualHere", "#F59E0B"),
        ("🎮 Cero Input Lag (Moonlight / Sunshine)", "#10B981"),
        ("🔌 Raspberry Pi + Windows 10/11 PnP", "#38BDF8"),
        ("🛡️ Drivers Certificados WHQL", "#A855F7")
    ] if lang == "es" else [
        ("⚡ $0 vs $49 VirtualHere License", "#F59E0B"),
        ("🎮 Zero Lag WSK (Moonlight / Sunshine)", "#10B981"),
        ("🔌 Raspberry Pi + Windows 10/11 PnP", "#38BDF8"),
        ("🛡️ WHQL Certified Drivers", "#A855F7")
    ]

    y = 340
    for txt, col in features:
        draw.rounded_rectangle([(80, y), (640, y + 54)], radius=12, fill="#1E293B", outline=col, width=2)
        draw.text((105, y + 12), txt, font=font_tag, fill="#F8FAFC")
        y += 70

    # Right Side: App Mockup / Screenshot
    app_img_path = os.path.join(ASSETS_DIR, "captures", "capture_01_mainwindow_dark.png")
    if not os.path.exists(app_img_path):
        app_img_path = os.path.join(ASSETS_DIR, "app_frame.png")

    if os.path.exists(app_img_path):
        try:
            app_im = Image.open(app_img_path)
            app_im.thumbnail((540, 520), Image.Resampling.LANCZOS)
            # Add subtle glow / border around app mockup
            ax, ay = 670, 110
            draw.rounded_rectangle([(ax - 6, ay - 6), (ax + app_im.width + 6, ay + app_im.height + 6)], radius=16, fill="#06B6D4")
            im.paste(app_im, (ax, ay))
        except Exception as e:
            print("Mockup error:", e)

    # Bottom Right Pill: "TUTORIAL COMPLETO"
    pill_text = "MASTERCLASS TUTORIAL v3.0"
    draw.rounded_rectangle([(700, 580), (1200, 640)], radius=14, fill="#0F2D37", outline="#06B6D4", width=3)
    draw.text((740, 595), pill_text, font=get_font(FONT_BOLD, 28), fill="#38BDF8")

    im.save(out_path, quality=95)
    print(f"✓ Thumbnail saved: {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == "__main__":
    t_es = os.path.join(RELEASE_DIR, "youtube_thumbnail_es.png")
    t_en = os.path.join(RELEASE_DIR, "youtube_thumbnail_en.png")
    create_thumbnail("es", t_es)
    create_thumbnail("en", t_en)
    # Also in docs/assets
    create_thumbnail("es", os.path.join(ASSETS_DIR, "youtube_thumbnail_16x9_es.png"))
    create_thumbnail("en", os.path.join(ASSETS_DIR, "youtube_thumbnail_16x9_en.png"))
