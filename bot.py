import os
import telebot

# 1. Ambil token dari Environment Variable Railway (atau gunakan token langsung jika variabel tidak ada)
TOKEN = os.getenv("8883789126:AAHpQbrJKMd1I8xKYpQT_C7LCUB1giQsXqE")

# 2. Inisialisasi bot menggunakan variabel TOKEN
bot = telebot.TeleBot("8883789126:AAHpQbrJKMd1I8xKYpQT_C7LCUB1giQsXqE")

# Chat ID Anda untuk notifikasi otomatis saat bot online
MY_CHAT_ID = "8684396228"

# 3. Notifikasi saat server Railway berhasil menyalakan bot
try:
    bot.send_message(
        MY_CHAT_ID,
        "🤖 **Bot Info Loker Ciayumajakuning Berhasil Online!**\n\nSistem siap menerima perintah.",
        parse_mode="Markdown"
    )
except Exception as e:
    print(f"Gagal mengirim pesan startup: {e}")

# 4. Handler Perintah /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "👋 Selamat datang di Bot Info Loker Ciayumajakuning!\n\n"
        "Ketik /help untuk melihat menu."
    )

# 5. Handler Perintah /help
@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.reply_to(
        message,
        "📌 **Menu Bantuan:**\n"
        "/start - Mulai bot\n"
        "/help - Bantuan\n"
        "/loker - Lowongan terbaru",
        parse_mode="Markdown"
    )

# 6. Handler Perintah /loker
@bot.message_handler(commands=['loker'])
def loker(message):
    bot.reply_to(
        message,
        "📢 Fitur lowongan sedang disiapkan."
    )

# 7. Jalankan Bot
if __name__ == '__main__':
    print("Bot aktif...")
    bot.infinity_polling(skip_pending=True)
