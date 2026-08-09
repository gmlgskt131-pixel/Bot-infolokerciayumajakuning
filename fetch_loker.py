import os
import re
import sys
import json
import time
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN", "8861664027:AAFhS__mhGD07rvyZ3Oyr8re0Tau8_lKw3w")
CHAT_ID = os.getenv("CHAT_ID", "-1004426208468")

RSS_FEEDS = [
    "https://rss.app/feeds/tebpd3uNK7QUF0yi.xml",
    "https://rss.app/feeds/MZMZkLtTiHKbr2ck.xml",
    "https://rss.app/feeds/7oEScJlZFeoYE3oo.xml"
]

IKLAN = "https://crypotential.com/kxseizepn?key=b27dbc018fb141e5773a6cc85f207c78"

# Database Anti-Duplikat
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
            print(f"Gagal mengambil RSS ({response.status_code})")
            continue

        root = ET.fromstring(response.content)
        items = root.findall(".//item")

        # Batasi maksimal 5 item teratas per feed per eksekusi untuk mencegah spam/rate limit
        for item in items[:5]:
            title = item.findtext("title", "").strip()
            link = item.findtext("link", "").strip()
            desc = item.findtext("description", "").strip()

            if not link or link in sent:
                continue

            desc = re.sub(r"<.*?>", "", desc).strip()

            pesan = f"""📢 *INFO LOKER TERBARU*

🏢 *{title}*

📝 {desc[:200]}...

🔗 *Lamar:* {link}

━━━━━━━━━━━━━━

🕒 *Update:* {datetime.now().strftime("%d-%m-%Y %H:%M")}

💰 *Penghasilan Tambahan*
👉 {IKLAN}

🤖 *INFO LOKER CIAYUMAJAKUNING*"""

            keyboard = {
                "inline_keyboard": [
                    [{"text": "📄 Lihat Lowongan", "url": link}],
                    [{"text": "💰 Penghasilan Tambahan", "url": IKLAN}]
                ]
            }

            # Menggunakan sendMessage (Lebih aman & tidak butuh link gambar yang valid)
            telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": CHAT_ID,
                "text": pesan,
                "parse_mode": "Markdown",
                "reply_markup": json.dumps(keyboard)
            }

            res = requests.post(telegram_url, json=payload, timeout=30)
            
            if res.status_code == 200:
                print(f"[BERHASIL] Sent: {title}")
                sent.append(link)
                # Jeda 3 detik antar pesan agar terhindar dari Error 429 (Too Many Requests)
                time.sleep(3)
            else:
                print(f"[GAGAL TELEGRAM] Status {res.status_code}: {res.text}")
                has_error = True

    except Exception as e:
        print(f"ERROR memproses {RSS_URL}: {e}")
        has_error = True

# Simpan database sent.json yang baru
with open("sent.json", "w") as f:
    json.dump(sent, f, indent=2)

if has_error:
    sys.exit(1)
    print("\nProses selesai dengan beberapa error.")
