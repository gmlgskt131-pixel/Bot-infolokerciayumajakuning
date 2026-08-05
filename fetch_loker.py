import os
import requests
import xml.etree.ElementTree as ET

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

RSS_URL = "https://rss.app/feeds/tebpd3uNK7QUF0yi.xml"

xml = requests.get(RSS_URL, timeout=30).text
root = ET.fromstring(xml)

items = root.findall(".//item")

for item in items[:5]:
    title = item.findtext("title", "")
    link = item.findtext("link", "")
    desc = item.findtext("description", "")

    pesan = f"""📢 INFO LOKER TERBARU

🏢 {title}

📝 {desc[:250]}

🔗 {link}

━━━━━━━━━━━━━━
🤖 INFO LOKER CIAYUMAJAKUNING
"""

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": pesan
        },
        timeout=30
    )
