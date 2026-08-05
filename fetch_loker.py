import os
import json
import requests
import feedparser

# Variabel Lingkungan dari GitHub Secrets & Script
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
HISTORY_FILE = "sent_posts.json"

# Daftar Feed RSS-Bridge dari beberapa akun Instagram Loker Ciayumajakuning
# Ganti URL di bawah dengan link RSS-Bridge asli hasil generate Anda
TARGET_FEEDS = [
    {
        "sumber": "Loker Cirebon",
        "url": "https://rss-bridge.org/bridge01/?action=display&bridge=InstagramBridge&u=infoloker.cirebon&format=Atom"
    },
    {
        "sumber": "Loker Indramayu",
        "url": "https://rss-bridge.org/bridge01/?action=display&bridge=InstagramBridge&u=infoloker.indramayu&format=Atom"
    },
    {
        "sumber": "Loker Majalengka",
        "url": "https://rss-bridge.org/bridge01/?action=display&bridge=InstagramBridge&u=infoloker.majalengka&format=Atom"
    }
]

def load_sent_history():
    """Membaca daftar ID postingan yang sudah pernah terkirim."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_sent_history(history):
    """Menyimpan ID postingan ke file JSON lokal."""
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

def format_caption(text):
    """Merapikan teks caption agar nyaman dibaca di Telegram."""
    clean_text = text.replace("<br>", "\n").replace("<br/>", "\n")
    if len(clean_text) > 600:
        clean_text = clean_text[:600] + "..."
    return clean_text

def send_telegram_message(sumber, title, link):
    """Mengirim format pesan profesional ke Telegram."""
    caption = format_caption(title)
    
    pesan = (
        f"📢 **INFO LOKER TERBARU** ({sumber})\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{caption}\n\n"
        f"🔗 [Klik untuk Lihat Detail / Melamar]({link})\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📲 *Dapatkan update loker harian gratis!*\n"
        f"👉 Join: {CHAT_ID}"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": pesan,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    
    res = requests.post(url, data=payload)
    return res.status_code == 200

def main():
    if not BOT_TOKEN or not CHAT_ID:
        print("Error: BOT_TOKEN atau CHAT_ID belum diset di Environment Variable!")
        return

    sent_history = load_sent_history()
    new_history = list(sent_history)

    for target in TARGET_FEEDS:
        print(f"Mengecek feed: {target['sumber']}...")
        feed = feedparser.parse(target["url"])

        # Ambil maksimal 3 postingan terbaru dari tiap sumber
        for entry in feed.entries[:3]:
            post_id = entry.get("id", entry.get("link"))

            # Jika postingan belum pernah dikirim
            if post_id not in sent_history:
                title = entry.get("title", "Informasi Loker")
                link = entry.get("link", "")

                success = send_telegram_message(target["sumber"], title, link)
                if success:
                    print(f"✅ Sukses terkirim: {post_id}")
                    new_history.append(post_id)
                else:
                    print(f"❌ Gagal mengirim: {post_id}")

    # Simpan maksimal 100 riwayat postingan terakhir
    save_sent_history(new_history[-100:])

if __name__ == "__main__":
    main()
  
