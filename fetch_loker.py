import os
import re
import sys
import json
import time
import html
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN", "8861664027:AAFhS__mhGD07rvyZ3Oyr8re0Tau8_lKw3w")
CHAT_ID = os.getenv("CHAT_ID", "8684396228")

# Masukkan daftar RSS yang aktif (URL 404 bisa dihapus atau diperbarui)
RSS_FEEDS = [
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

def clean_text(raw_text):
    if not raw_text:
        return ""
    # Hapus tag HTML
    text = re.sub(r"<.*?>", "", raw_text)
    # Hapus whitespace berlebih
    text = " ".join(text.split())
    # Escape karakter khusus HTML agar tidak crash di Telegram HTML parser
    return html.escape(text)

for RSS_URL in RSS_FEEDS:
    try:
        print(f"Mengambil RSS Feed: {RSS_URL}")
        response = requests.get(RSS_URL, timeout=30)
        
        if response.status_code != 200:
            print(f"Gagal mengambil RSS ({response.status_code}) - Lewati feed ini.")
            continue

        root = ET.fromstring(response.content)
        items = root.findall(".//item")

        for item in items[:5]:  # Ambil maksimal 5 item per feed
            title_raw = item.findtext("title", "")
            link_raw = item.findtext("link", "")
            desc_raw = item.findtext("description", "")

            if not link_raw or link_raw in sent:
                continue

            title = clean_text(title_raw)
            link = link_raw.strip()
            desc = clean_text(desc_raw)

            # Jika deskripsi terlalu pendek/kosong, gunakan ringkasan dari judul
            if len(desc) < 10:
                desc = "Klik tombol 'Lihat Lowongan' di bawah untuk detail kualifikasi dan cara melamar."

            pesan = f"""📢 <b>INFO LOKER TERBARU</b>

🏢 <b>{title}</b>

📝 {desc[:350]}...

━━━━━━━━━━━━━━

🕒 <b>Update:</b> {datetime.now().strftime("%d-%m-%Y %H:%M")}

💰 <b>Penghasilan Tambahan</b>
👉 {IKLAN}

🤖 <b>INFO LOKER CIAYUMAJAKUNING</b>"""

            keyboard = {
                "inline_keyboard": [
                    [{"text": "📄 Lihat Lowongan", "url": link}],
                    [{"text": "💰 Penghasilan Tambahan", "url": IKLAN}]
                ]
            }

            telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": CHAT_ID,
                "text": pesan,
                "parse_mode": "HTML",  # Ganti dari Markdown ke HTML
                "reply_markup": json.dumps(keyboard),
                "disable_web_page_preview": True  # Mencegah preview link merusak tampilan
            }

            res = requests.post(telegram_url, json=payload, timeout=30)
            
            if res.status_code == 200:
                print(f"[BERHASIL] Sent: {title_raw[:30]}...")
                sent.append(link)
                time.sleep(3)  # Jeda anti rate limit
            else:
                print(f"[GAGAL TELEGRAM] Status {res.status_code}: {res.text}")
                has_error = True

    except Exception as e:
        print(f"ERROR memproses {RSS_URL}: {e}")
        has_error = True

# Simpan database sent.json
with open("sent.json", "w") as f:
    json.dump(sent, f, indent=2)

if has_error:
    sys.exit(1)
