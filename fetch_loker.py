import os
import re
import requests
import xml.etree.ElementTree as ET

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

IKLAN = "https://crypotential.com/kxseizepn?key=b27dbc018fb141e5773a6cc85f207c78"
RSS_URL = "https://rss.app/feeds/MZMZkLtTiHKbr2ck.xml"

xml = requests.get(RSS_URL, timeout=30).text
root = ET.fromstring(xml)

items = root.findall(".//item")

for item in items[:5]:
    title = item.findtext("title", "")
    link = item.findtext("link", "")
    desc = item.findtext("description", "")

    # Hapus semua tag HTML
    desc = re.sub(r"<.*?>", "", desc).strip()

    pesan = f"""📢 INFO LOKER TERBARU

🏢 {title}

📝 {desc[:250]}

🔗 Link Lowongan:
{link}

━━━━━━━━━━━━━━

💰 Ingin mendapatkan penghasilan tambahan dari HP?

👉 {IKLAN}

━━━━━━━━━━━━━━
🤖 INFO LOKER CIAYUMAJAKUNING
"""

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": pesan,
            "disable_web_page_preview": False
        },
        timeout=30
    )
