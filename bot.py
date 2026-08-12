import os
import telebot
from telebot import types


# =========================
# CONFIG
# =========================

BOT_TOKEN = (
    os.getenv("BOT_TOKEN")
    or os.getenv("TOKEN_BOT")
    or ""
).strip()
MY_CHAT_ID = (
    os.getenv("MY_CHAT_ID")
    or os.getenv("CHAT_ID")
    or os.getenv("TELEGRAM_CHAT_ID")
    or ""
).strip()

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN tidak ditemukan. "
        "Masukkan BOT_TOKEN di Railway Variables."
    )


# =========================
# INIT BOT
# =========================

bot = telebot.TeleBot(
    BOT_TOKEN,
    parse_mode="HTML"
)


# =========================
# HANDLERS
# =========================

def main_menu():
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2
    )
    keyboard.add(
        types.KeyboardButton("/start"),
        types.KeyboardButton("/help"),
        types.KeyboardButton("/loker"),
        types.KeyboardButton("/admin")
    )
    return keyboard


@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.reply_to(
        message,
        (
            "👋 Selamat datang di Bot <b>KerjaDimana.id</b>!\n\n"
            "Ketik /help untuk melihat menu."
        ),
        reply_markup=main_menu()
    )


@bot.message_handler(commands=["help"])
def handle_help(message):
    bot.reply_to(
        message,
        (
            "📌 <b>Menu Bantuan:</b>\n"
            "/start - Mulai bot\n"
            "/help - Bantuan\n"
            "/loker - Lowongan terbaru\n"
            "/admin - Info admin"
        ),
        reply_markup=main_menu()
    )


@bot.message_handler(commands=["loker"])
def handle_loker(message):
    bot.reply_to(
        message,
        (
            "📢 Info lowongan terbaru dikirim otomatis ke channel/grup "
            "KerjaDimana.id.\n\n"
            "Pantau terus update dari bot ini ya."
        ),
        reply_markup=main_menu()
    )


@bot.message_handler(commands=["admin"])
def handle_admin(message):
    bot.reply_to(
        message,
        "Admin KerjaDimana.id siap membantu. Kirim pesan kebutuhan kamu di sini.",
        reply_markup=main_menu()
    )


@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    bot.reply_to(
        message,
        "Perintah belum dikenali. Ketik /help untuk melihat menu.",
        reply_markup=main_menu()
    )


def main():
    print("=" * 50)
    print("KerjaDimana.id Bot")
    print("BOT AKTIF")
    print("=" * 50)

    bot.infinity_polling(
        timeout=30,
        long_polling_timeout=30,
        skip_pending=True
    )


if __name__ == "__main__":
    main()
