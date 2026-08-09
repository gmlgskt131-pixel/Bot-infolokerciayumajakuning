import os
import re
import sys
import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# 1. Cara pengambilan Token & Chat ID yang benar
# Nilai rahasia dimasukkan langsung atau diambil dari nama Environment Variable di GitHub Secrets
BOT_TOKEN = os.getenv("BOT_TOKEN", "8861664027:AAFhS__mhGD07rvyZ3Oyr8re0Tau8_lKw3w")
CHAT_ID = os.getenv("CHAT_ID", "-1004426208468")

RSS_FEEDS = [
    "https://rss.app/feeds/tebpd3uNK7QUF0yi.xml",
    "https://rss.app/feeds/MZMZkLtTiHKbr2ck.xml",
    "https://rss.app/feeds/7oEScJlZFeoYE3oo.xml"
]

LOGO_URL = "https://i.ibb.co/xxxxxxxx/logo.png"
IKLAN = "https://crypotential.com/kxseizepn?key=b27dbc018fb141e5773a6cc85f207c78"

# 2. Database Anti-Duplikat
try:
    with open("sent.json", "r") as f:
        sent = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    sent = []

has_error = False

for RSS_URL in RSS_FEEDS:
    try:
        print(f"Mengambil RSS Feed: {RSS_URL}")
        response = requests.get(RSS_URL, timeout=30)
        
        if response.status_code != 200:
            print(f"Gagal mengambil RSS ({response.status_code}): {RSS_URL}")
            continue

        # Parsing XML secara aman
        root = ET.fromstring(response.content)
        items = root.findall(".//item")

        for item in items:
            title = item.findtext("title", "").strip()
            link = item.findtext("link", "").strip()
            desc = item.findtext("description", "").strip()

            if not link or link in sent:
                continue

            # Clean HTML tag dari deskripsi
            desc = re.sub(r"<.*?>", "", desc).strip()

            pesan = f"""📢 INFO LOKER TERBARU

🏢 {title}

📝 {desc[:250]}...

🔗 Lamar:
{link}

━━━━━━━━━━━━━━

🕒 Update:
{datetime.now().strftime("%d-%m-%Y %H:%M")}

💰 Penghasilan Tambahan
👉 {IKLAN}

🤖 INFO LOKER CIAYUMAJAKUNING"""

            keyboard = {
                "inline_keyboard": [
                    [{"text": "📄 Lihat Lowongan", "url": link}],
                    [{"text": "💰 Penghasilan Tambahan", "url": IKLAN}]
                ]
            }

            # Kirim Ke Telegram
            telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            payload = {
                "chat_id": CHAT_ID,
                "photo": LOGO_URL,
                "caption": pesan,
                "reply_markup": json.dumps(keyboard)
            }

            res = requests.post(telegram_url, data=payload, timeout=30)
            
            if res.status_code == 200:
                print(f" [BERHASIL] Sent: {title}")
                sent.append(link)
            else:
                print(f" [GAGAL TELEGRAM] Status {res.status_code}: {res.text}")
                has_error = True

    except Exception as e:
        print(f"ERROR memproses {RSS_URL}: {e}")
        has_error = True

# 3. Simpan database anti-duplikat
with open("sent.json", "w") as f:
    json.dump(sent, f, indent=2)

# Jika ada error selama proses, hentikan dengan exit code 1 agar GitHub Actions memberitahukan tanda merah
if has_error:
    print("\nProses selesai dengan beberapa error.")
