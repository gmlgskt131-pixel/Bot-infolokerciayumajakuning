import os
import re
import sys
import json
import time
import html
import requests
import xml.etree.ElementTree as ET


# =========================================================
# CONFIG
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

CHAT_ID = (
    os.getenv("CHAT_ID")
    or os.getenv("TELEGRAM_CHAT_ID")
    or ""
).strip()

RSS_FEEDS = [
    "https://rss.app/feeds/MZMZkLtTiHKbr2ck.xml",
    "https://rss.app/feeds/7oEScJlZFeoYE3oo.xml",
]

IKLAN = "https://crypotential.com/kxseizepn?key=b27dbc018fb141e5773a6cc85f207c78"

SENT_FILE = "sent.json"


# =========================================================
# VALIDASI
# =========================================================

if not BOT_TOKEN:
    print("❌ BOT_TOKEN tidak ditemukan!")
    sys.exit(1)

if not CHAT_ID:
    print("❌ CHAT_ID tidak ditemukan!")
    sys.exit(1)

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


# =========================================================
# DATABASE ANTI DUPLIKAT
# =========================================================

def load_sent():
    try:
        with open(SENT_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data

    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return []


def save_sent(sent):
    with open(SENT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            sent,
            file,
            ensure_ascii=False,
            indent=2
        )


# =========================================================
# CLEAN TEXT
# =========================================================

def clean_text(raw_text):
    if not raw_text:
        return ""

    text = re.sub(r"<[^>]+>", " ", raw_text)
    text = html.unescape(text)
    text = " ".join(text.split())

    return html.escape(text)


# =========================================================
# KIRIM KE TELEGRAM
# =========================================================

def send_telegram(title, description, link):

    # Hindari pesan melebihi batas Telegram
    if len(description) > 3000:
        description = description[:3000] + "..."

    pesan = (
        "📢 <b>INFO LOKER TERBARU</b>\n\n"
        f"🏢 <b>{title}</b>\n\n"
        "📝 <b>Deskripsi Pekerjaan</b>\n"
        f"{description}\n\n"
        "━━━━━━━━━━━━━━\n\n"
        "💰 <b>Penghasilan Tambahan</b>\n"
        f"👉 {IKLAN}\n\n"
        "🤖 <b>KerjaDimana.id</b>"
    )

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

    payload = {
        "chat_id": CHAT_ID,
        "text": pesan,
        "parse_mode": "HTML",
        "reply_markup": keyboard,
        "disable_web_page_preview": True
    }

    try:
        response = requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json=payload,
            timeout=30
        )

        data = response.json()

        if response.status_code == 200 and data.get("ok"):
           print(...)
           return True
        print("❌ GAGAL TELEGRAM")
        print(f"HTTP Status: {response.status_code}")
        print(f"Response: {response.text}")

        return False

    except requests.RequestException as error:
        print(f"❌ Telegram request error: {error}")
        return False


# =========================================================
# PROSES RSS
# =========================================================

def process_feed(rss_url, sent):

    print()
    print("=" * 60)
    print(f"📡 Mengambil RSS: {rss_url}")

    try:
        response = requests.get(
            rss_url,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0 KerjaDimanaBot/1.0"
            }
        )

    except requests.RequestException as error:
        print(f"❌ Gagal mengambil RSS: {error}")
        return 0

    if response.status_code != 200:
        print(
            f"⚠️ RSS HTTP {response.status_code}. "
            "Feed dilewati."
        )
        return 0

    try:
        root = ET.fromstring(response.content)

    except ET.ParseError as error:
        print(f"❌ XML RSS rusak: {error}")
        return 0

    items = root.findall(".//item")

    print(f"📦 Ditemukan {len(items)} item.")

    jumlah_berhasil = 0

    for item in items[:5]:

        title_raw = item.findtext("title", "")
        link_raw = item.findtext("link", "")
        desc_raw = item.findtext("description", "")

        link = (link_raw or "").strip()

        if not link:
            continue

        if link in sent:
            print(f"⏭️ Sudah dikirim: {title_raw[:60]}")
            continue

        title = clean_text(title_raw)
        description = clean_text(desc_raw)

        if not title:
            title = "Lowongan Kerja Terbaru"

        if len(description) < 10:
            description = (
                "Klik tombol Lihat Lowongan untuk melihat "
                "informasi lengkap, kualifikasi, dan cara melamar."
            )

        print(f"📨 Mengirim: {html.unescape(title)[:70]}")

        berhasil = send_telegram(
            title,
            description,
            link
        )

        if berhasil:
            sent.append(link)
            save_sent(sent)

            jumlah_berhasil += 1

            time.sleep(2)

    return jumlah_berhasil


# =========================================================
# MAIN
# =========================================================

def main():

    sent = load_sent()

    print("=" * 60)
    print("🤖 KerjaDimana.id Auto Loker")
    print(f"📢 CHAT_ID: {CHAT_ID}")
    print(f"📚 Sudah tersimpan: {len(sent)} lowongan")
    print("=" * 60)

    total = 0

    for rss_url in RSS_FEEDS:
        total += process_feed(
            rss_url,
            sent
        )

    save_sent(sent)

    print()
    print("=" * 60)
    print(f"✅ SELESAI — {total} lowongan baru dikirim.")
    print("=" * 60)


if __name__ == "__main__":
    main()
