import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

pesan = """
📢 INFO LOKER CIAYUMAJAKUNING

🤖 Bot berhasil berjalan melalui GitHub Actions.

Ini adalah pesan uji otomatis.
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": pesan
    }
)
