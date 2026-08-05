import os
import re
import requests
import xml.etree.ElementTree as ET

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

RSS_URL = "https://rss.app/feeds/tebpd3uNK7QUF0yi.xml"

LOGO_URL = "https://i.ibb.co/xxxxxxxx/logo.png"

IKLAN = "https://crypotential.com/kxseizepn?key=b27dbc018fb141e5773a6cc85f207c78"

xml = requests.get(RSS_URL, timeout=30).text
root = ET.fromstring(xml)

items = root.findall(".//item")

for item in items[:5]:
    title = item.findtext("title", "")
    link = item.findtext("link", "")
    desc = item.findtext("description", "")

    # Hapus HTML
    desc = re.sub(r"<.*?>", "", desc).strip()

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

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
        data={
            "chat_id": CHAT_ID,
            "photo": LOGO_URL,
            "caption": pesan
        },
        timeout=30
    )
👉 {IKLAN}

━━━━━━━━━━━━━━
🤖 INFO LOKER CIAYUMAJAKUNING
"""

    requests.post(
        requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
    data={
        "chat_id": CHAT_ID,
        "photo": "https://i.ibb.co/qLyBh0p3/logo.png",
        "caption": pesan
    },
    timeout=30
)
