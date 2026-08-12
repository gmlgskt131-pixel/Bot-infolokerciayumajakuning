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

BOT_TOKEN = os.getenv("BOT_TOKEN", "8883789126:AAFWOh2bW2-ch1in3GEDK04GSxdBKPhn6tw").strip()

# Bisa membaca CHAT_ID atau TELEGRAM_CHAT_ID
CHAT_ID = (
    os.getenv("CHAT_ID")
    or os.getenv("TELEGRAM_CHAT_ID")
    or "-1004426208468"
).strip()

TELEGRAM_API = f"https://api.telegram.org/bot{8883789126:AAFWOh2bW2-ch1in3GEDK04GSxdBKPhn6tw}"

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
    print("Tambahkan BOT_TOKEN ke GitHub Secrets.")
    sys.exit(1)

if not CHAT_ID:
    print("❌ CHAT_ID tidak ditemukan!")
    sys.exit(1)

print("=" * 60)
print("🤖 KerjaDimana.id Auto Loker")
print(f"📢 CHAT_ID: {CHAT_ID}")
print("=" * 60)


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


sent = load_sent()


# =========================================================
# BERSIHKAN TEXT RSS
# =========================================================

def clean_text(raw_text):
    if not raw_text:
        return ""

    # Hapus tag HTML
    text = re.sub(r"<[^>]+>", " ", raw_text)

    # Decode HTML entity
    text = html.unescape(text)

    # Hilangkan whitespace berlebih
    text = " ".join(text.split())

    # Amankan untuk parse_mode HTML Telegram
    return html.escape(text)


# =========================================================
# PECAH DESKRIPSI PANJANG
# =========================================================

def split_text(text, max_length=2500):
    if not text:
        return [""]

    words = text.split()
    chunks = []
    current = ""

    for word in words:
        candidate = f"{current} {word}".strip()

        if len(candidate) <= max_length:
            current = candidate
        else:
            if current:
                chunks.append(current)

            current = word

    if current:
        chunks.append(current)

    return chunks or [""]


# =========================================================
# KIRIM LOWONGAN KE TELEGRAM
# =========================================================

def send_telegram(title, description, link):
    description_parts = split_text(description)

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

    total_parts = len(description_parts)

    for index, part in enumerate(description_parts):
        is_first = index == 0
        is_last = index == total_parts - 1

        pesan = ""

        if is_first:
            pesan += (
                "📢 <b>INFO KerjaDimana.id</b>\n\n"
                f"🏢 <b>{title}</b>\n\n"
                "📝 <b>Deskripsi Pekerjaan</b>\n"
            )
        else:
            pesan += "📝 <b>Lanjutan Deskripsi</b>\n"

        pesan += part

        if is_last:
            pesan += (
                "\n\n━━━━━━━━━━━━━━\n\n"
                "💰 <b>Penghasilan Tambahan</b>\n"
                f"👉 {IKLAN}\n\n"
                "🤖 <b>KerjaDimana.id</b>"
            )

        payload = {
            "chat_id": CHAT_ID,
            "text": pesan,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }

        # Tombol hanya muncul pada pesan terakhir
        if is_last:
            payload["reply_markup"] = keyboard

        try:
            res = requests.post(
                f"{TELEGRAM_API}/sendMessage",
                json=payload,
                timeout=30
            )

        except requests.RequestException as error:
            print(f"❌ Gagal terhubung ke Telegram: {error}")
            return False

        try:
            data = res.json()
        except ValueError:
            print("❌ Telegram mengembalikan response bukan JSON.")
            print(res.text)
            return False

        if res.status_code != 200 or not data.get("ok"):
            print("❌ GAGAL TELEGRAM")
            print(f"HTTP Status : {res.status_code}")
            print(f"Response    : {res.text}")
            return False

        # Jeda jika deskripsi terdiri dari beberapa pesan
        if not is_last:
            time.sleep(1)

    print(f"✅ BERHASIL: {html.unescape(title)[:70]}")
    return True


# =========================================================
# PROSES RSS
# =========================================================

def process_feed(rss_url):
    print()
    print("=" * 60)
    print(f"📡 Mengambil RSS Feed:")
    print(rss_url)

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
        return False

    if response.status_code != 200:
        print(
            f"⚠️ RSS gagal. HTTP {response.status_code}. "
            "Feed dilewati."
        )
        return False

    try:
        root = ET.fromstring(response.content)

    except ET.ParseError as error:
        print(f"❌ XML RSS tidak valid: {error}")
        return False

    items = root.findall(".//item")

    print(f"📦 Ditemukan {len(items)} item.")

    if not items:
        print("⚠️ RSS tidak memiliki item.")
        return True

    jumlah_baru = 0

    # Maksimal 5 lowongan per feed setiap run
    for item in items[:5]:
        title_raw = item.findtext("title", "")
        link_raw = item.findtext("link", "")
        desc_raw = item.findtext("description", "")

        link = (link_raw or "").strip()

        if not link:
            print("⏭️ Item tidak punya link. Dilewati.")
            continue

        # Anti duplikat
        if link in sent:
            print(
                f"⏭️ Sudah pernah dikirim: "
                f"{title_raw[:60]}"
            )
            continue

        title = clean_text(title_raw)
        description = clean_text(desc_raw)

        if not title:
            title = "Lowongan Kerja Terbaru"

        if len(description) < 10:
            description = (
                "Klik tombol Lihat Lowongan di bawah "
                "untuk melihat detail pekerjaan, "
                "kualifikasi, dan cara melamar."
            )

        print()
        print(f"📨 Mengirim: {html.unescape(title)[:70]}")

        berhasil = send_telegram(
            title,
            description,
            link
        )

        if berhasil:
            sent.append(link)
            save_sent(sent)

            jumlah_baru += 1

            # Jeda agar tidak terlalu cepat mengirim
            time.sleep(2)

    print()
    print(
        f"✅ Feed selesai. "
        f"{jumlah_baru} lowongan baru dikirim."
    )

    return True


# =========================================================
# MAIN
# =========================================================

def main():
    has_error = False

    print(f"📚 Database anti-duplikat: {len(sent)} link.")

    for rss_url in RSS_FEEDS:
        sukses = process_feed(rss_url)

        if not sukses:
            has_error = True

    save_sent(sent)

    print()
    print("=" * 60)
    print("✅ PROSES SELESAI")
    print(f"📚 Total link tersimpan: {len(sent)}")
    print("=" * 60)

    # RSS yang error tidak perlu membuat seluruh Actions gagal.
    # Ubah menjadi sys.exit(1) jika ingin workflow merah saat RSS gagal.
    if has_error:
        print("⚠️ Ada satu atau lebih RSS yang bermasalah.")


if __name__ == "__main__":
    main()
