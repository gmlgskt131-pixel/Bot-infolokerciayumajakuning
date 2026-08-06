import os
import re
import requests
import xml.etree.ElementTree as ET

# Ambil dari GitHub Secrets
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# RSS Feed
RSS_URL = "https://rss.app/feeds/tebpd3uNK7QUF0yi.xml"

# Logo (ganti dengan direct link gambar)
LOGO_URL = "https://i.ibb.co/xxxxxxxx/logo.png"

# Link iklan
IKLAN = "https://crypotential.com/kxseizepn?key=b27dbc018fb141e5773a6cc85f207c78"

# Ambil RSS
xml = requests.get(RSS_URL, timeout=30).text
root = ET.fromstring(xml)

# Ambil 5 postingan terbaru
items = root.findall(".//item")[:5]

for item in items:

    title = item.findtext("title", "Tanpa Judul")
    link = item.findtext("link", "")
    desc = item.findtext("description", "")

    # Bersihkan HTML
    desc = re.sub(r"<.*?>", "", desc)
    desc = desc.strip()

    pesan = f"""📢 INFO LOKER TERBARU

🏢 {title}

📝 {desc[:250]}

🔗 Link Lowongan:
{link}

━━━━━━━━━━━━━━

💰 Ingin mendapatkan penghasilan tambahan dari HP?

👉 {IKLAN}

🤖 INFO LOKER CIAYUMAJAKUNING
"""

    # Kirim foto + caption ke Telegram
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
        data={
            "chat_id": CHAT_ID,
            "photo": LOGO_URL,
            "caption": pesan
        },
        timeout=30
    )
