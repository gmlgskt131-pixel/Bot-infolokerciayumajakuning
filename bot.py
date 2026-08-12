import os
import telebot
from telebot import types


# =========================
# CONFIG
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN", "8883789126:AAFWOh2bW2-ch1in3GEDK04GSxdBKPhn6tw").strip()
MY_CHAT_ID = os.getenv("MY_CHAT_ID", "-1004426208468").strip()

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
