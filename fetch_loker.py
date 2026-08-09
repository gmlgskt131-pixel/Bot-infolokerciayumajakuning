import os
import re
import requests
import xml.etree.ElementTree as ET
import json
from datetime import datetime

BOT_TOKEN = os.getenv("8861664027:AAFhS__mhGD07rvyZ3Oyr8re0Tau8_lKw3w")
CHAT_ID = os.getenv("-1004426208468")

RSS_FEEDS = [
    "https://rss.app/feeds/tebpd3uNK7QUF0yi.xml",
    "https://rss.app/feeds/MZMZkLtTiHKbr2ck.xml",
    "https://rss.app/feeds/7oEScJlZFeoYE3oo.xml"
]

LOGO_URL = "https://i.ibb.co/xxxxxxxx/logo.png"

IKLAN = "https://crypotential.com/kxseizepn?key=b27dbc018fb141e5773a6cc85f207c78"

# Database anti duplikat
try:
    with open("sent.json", "r") as f:
        sent = json.load(f)
except:
    sent = []

for RSS_URL in RSS_FEEDS:

    try:
        xml = requests.get(RSS_URL, timeout=30).text
        root = ET.fromstring(xml)
        items = root.findall(".//item")

        for item in items:

            title = item.findtext("title", "")
            link = item.findtext("link", "")
            desc = item.findtext("description", "")

            if link in sent:
                continue

            desc = re.sub(r"<.*?>", "", desc).strip()

            pesan = f"""📢 INFO LOKER TERBARU

🏢 {title}

📝 {desc[:250]}

🔗 Lamar:
{link}

━━━━━━━━━━━━━━

🕒 Update:
{datetime.now().strftime("%d-%m-%Y %H:%M")}

💰 Penghasilan Tambahan
👉 {IKLAN}

🤖 INFO LOKER CIAYUMAJAKUNING
"""

            keyboard = {
                "inline_keyboard": [
                    [
                        {
                            "text": "📄 Lihat Lowongan",
                            "url": link
                        }
                    ],
                    [
                        {
                            "text": "💰 Penghasilan Tambahan",
                            "url": IKLAN
                        }
                    ]
                ]
            }

            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                data={
                    "chat_id": CHAT_ID,
                    "photo": LOGO_URL,
                    "caption": pesan,
                    "reply_markup": json.dumps(keyboard)
                },
                timeout=30
            )

            sent.append(link)

        with open("sent.json", "w") as f:
            json.dump(sent, f)

    except Exception as e:
        print("ERROR:", e)
