import os
import telebot

# 1. Mengambil token dari Environment Variable Railway (Gunakan Key: TELEGRAM_TOKEN)
# Jika tidak ada variable, fallback ke token langsung dalam tanda petik
TOKEN = os.getenv("8883789126:AAHpQbrJKMd1I8xKYpQT_C7LCUB1giQsXqE")

bot = telebot.TeleBot("8883789126:AAHpQbrJKMd1I8xKYpQT_C7LCUB1giQsXqE")

# Chat ID Anda untuk notifikasi otomatis
MY_CHAT_ID = "8684396228"

# 2. Pesan otomatis dikirim langsung ke Telegram Anda saat bot Railway aktif
try:
    bot.send_message(
        MY_CHAT_ID,
        "🤖 **Bot Info Loker Ciayumajakuning Berhasil Online!**\n\nSistem siap menerima perintah.",
        parse_mode="Markdown"
    )
except Exception as e:
    print(f"Gagal mengirim pesan startup: {e}")

# 3. Handler Perintah Telegram
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "👋 Selamat datang di Bot Info Loker Ciayumajakuning!\n\n"
        "Ketik /help untuk melihat menu."
    )

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

@bot.message_handler(commands=['loker'])
def loker(message):
    bot.reply_to(
        message,
        "📢 Fitur lowongan sedang disiapkan."
    )

# 4. Jalankan Bot
if __name__ == '__main__':
    print("Bot aktif...")
    bot.infinity_polling(skip_pending=True)

