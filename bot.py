import os
import telebot

BOT_TOKEN = os.getenv("83789126:AAFs-YoNg2oBvtkezZAcveq-1qmBMrDIkIE")

bot = telebot.TeleBot(8883789126:AAFs-YoNg2oBvtkezZAcveq-1qmBMrDIkIE)

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
        "/start - Mulai bot\n"
        "/help - Bantuan\n"
        "/loker - Lowongan terbaru"
    )

@bot.message_handler(commands=['loker'])
def loker(message):
    bot.reply_to(
        message,
        "📢 Fitur lowongan sedang disiapkan."
    )

print("Bot aktif...")
bot.infinity_polling(skip_pending=True)
