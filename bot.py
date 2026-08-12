import os
import telebot
from telebot import types


# =========================================================
# CONFIG
# =========================================================

TOKEN_TOKEN = os.getenv("8883789126:AAFWOh2bW2-ch1in3GEDK04GSxdBKPhn6tw")
MY_CHAT_ID = os.getenv"-1004426208468"
if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN tidak ditemukan. "
        "Masukkan BOT_TOKEN di Railway Variables."
    )


# =========================================================
# INIT BOT
# =========================================================

bot = telebot.TeleBot(
    BOT_TOKEN,
    parse_mode="HTML"
)


# =========================================================
# MENU UTAMA
# =========================================================

def main_menu():
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    keyboard.add(
        types.InlineKeyboardButton(
            "🆕 Lowongan Terbaru",
            callback_data="loker"
        ),
        types.InlineKeyboardButton(
            "🔎 Cari Lowongan",
            callback_data="cari"
        )
    )

    keyboard.add(
        types.InlineKeyboardButton(
            "📍 Lokasi",
            callback_data="lokasi"
        ),
        types.InlineKeyboardButton(
            "💼 Kategori",
            callback_data="kategori"
        )
    )

    keyboard.add(
        types.InlineKeyboardButton(
            "📢 Channel KerjaDimana.id",
            url="https://t.me/KerjaDimana_id"
        )
    )

    keyboard.add(
        types.InlineKeyboardButton(
            "ℹ️ Bantuan",
            callback_data="help"
        )
    )

    return keyboard


# =========================================================
# /START
# =========================================================

@bot.message_handler(commands=["start"])
def start(message):
    nama = message.from_user.first_name or "Kak"

    text = (
        f"👋 <b>Halo {nama}!</b>\n\n"
        "Selamat datang di <b>KerjaDimana.id</b> 🚀\n\n"
        "Temukan informasi lowongan kerja terbaru "
        "dengan cepat dan mudah.\n\n"
        "Silakan pilih menu di bawah 👇"
    )

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=main_menu()
    )


# =========================================================
# /HELP
# =========================================================

@bot.message_handler(commands=["help"])
def help_cmd(message):
    text = (
        "ℹ️ <b>Menu Bantuan KerjaDimana.id</b>\n\n"
        "🏠 /start — Menu utama\n"
        "🆕 /loker — Lowongan terbaru\n"
        "🔎 /cari — Cari lowongan\n"
        "📍 /lokasi — Berdasarkan lokasi\n"
        "💼 /kategori — Berdasarkan kategori\n"
        "ℹ️ /help — Bantuan\n\n"
        "📢 Channel resmi:\n"
        "@KerjaDimana_id"
    )

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=main_menu()
    )


# =========================================================
# /LOKER
# =========================================================

@bot.message_handler(commands=["loker"])
def loker(message):
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(
        types.InlineKeyboardButton(
            "📢 Lihat Lowongan Terbaru",
            url="https://t.me/KerjaDimana_id"
        )
    )

    keyboard.add(
        types.InlineKeyboardButton(
            "🏠 Menu Utama",
            callback_data="menu"
        )
    )

    bot.send_message(
        message.chat.id,
        (
            "🆕 <b>Lowongan Kerja Terbaru</b>\n\n"
            "Informasi lowongan terbaru tersedia di "
            "<b>KerjaDimana.id</b>.\n\n"
            "Klik tombol di bawah 👇"
        ),
        reply_markup=keyboard
    )


# =========================================================
# /CARI
# =========================================================

@bot.message_handler(commands=["cari"])
def cari(message):
    bot.send_message(
        message.chat.id,
        (
            "🔎 <b>Cari Lowongan</b>\n\n"
            "Ketik nama pekerjaan yang kamu cari.\n\n"
            "Contoh:\n"
            "• Operator Produksi\n"
            "• Admin\n"
            "• Staff Gudang\n"
            "• Sales\n\n"
            "🚧 Fitur pencarian database akan "
            "diaktifkan pada tahap berikutnya."
        ),
        reply_markup=main_menu()
    )


# =========================================================
# /LOKASI
# =========================================================

@bot.message_handler(commands=["lokasi"])
def lokasi(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    keyboard.add(
        types.InlineKeyboardButton(
            "📍 Cirebon",
            callback_data="loc_cirebon"
        ),
        types.InlineKeyboardButton(
            "📍 Indramayu",
            callback_data="loc_indramayu"
        )
    )

    keyboard.add(
        types.InlineKeyboardButton(
            "📍 Majalengka",
            callback_data="loc_majalengka"
        ),
        types.InlineKeyboardButton(
            "📍 Kuningan",
            callback_data="loc_kuningan"
        )
    )

    keyboard.add(
        types.InlineKeyboardButton(
            "🏠 Menu Utama",
            callback_data="menu"
        )
    )

    bot.send_message(
        message.chat.id,
        "📍 <b>Pilih lokasi pekerjaan:</b>",
        reply_markup=keyboard
    )


# =========================================================
# /KATEGORI
# =========================================================

@bot.message_handler(commands=["kategori"])
def kategori(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    keyboard.add(
        types.InlineKeyboardButton(
            "🏭 Operator",
            callback_data="cat_operator"
        ),
        types.InlineKeyboardButton(
            "📋 Admin",
            callback_data="cat_admin"
        )
    )

    keyboard.add(
        types.InlineKeyboardButton(
            "💰 Sales",
            callback_data="cat_sales"
        ),
        types.InlineKeyboardButton(
            "💻 IT",
            callback_data="cat_it"
        )
    )

    keyboard.add(
        types.InlineKeyboardButton(
            "🏠 Menu Utama",
            callback_data="menu"
        )
    )

    bot.send_message(
        message.chat.id,
        "💼 <b>Pilih kategori pekerjaan:</b>",
        reply_markup=keyboard
    )


# =========================================================
# CALLBACK BUTTON
# =========================================================

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    try:
        bot.answer_callback_query(call.id)
    except Exception:
        pass

    if call.data == "menu":
        bot.edit_message_text(
            "🏠 <b>Menu Utama KerjaDimana.id</b>\n\n"
            "Silakan pilih menu di bawah 👇",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu()
        )

    elif call.data == "loker":
        keyboard = types.InlineKeyboardMarkup()

        keyboard.add(
            types.InlineKeyboardButton(
                "📢 Buka Channel Lowongan",
                url="https://t.me/KerjaDimana_id"
            )
        )

        keyboard.add(
            types.InlineKeyboardButton(
                "🏠 Menu Utama",
                callback_data="menu"
            )
        )

        bot.edit_message_text(
            "🆕 <b>Lowongan Terbaru</b>\n\n"
            "Klik tombol di bawah untuk melihat "
            "lowongan terbaru.",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
        )

    elif call.data == "cari":
        keyboard = types.InlineKeyboardMarkup()

        keyboard.add(
            types.InlineKeyboardButton(
                "🏠 Menu Utama",
                callback_data="menu"
            )
        )

        bot.edit_message_text(
            "🔎 <b>Cari Lowongan</b>\n\n"
            "Ketik nama pekerjaan yang kamu cari.\n\n"
            "Contoh:\n"
            "• Operator Produksi\n"
            "• Admin Gudang\n"
            "• Sales",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
        )

    elif call.data == "lokasi":
        keyboard = types.InlineKeyboardMarkup(row_width=2)

        keyboard.add(
            types.InlineKeyboardButton(
                "📍 Cirebon",
                callback_data="loc_cirebon"
            ),
            types.InlineKeyboardButton(
                "📍 Indramayu",
                callback_data="loc_indramayu"
            )
        )

        keyboard.add(
            types.InlineKeyboardButton(
                "📍 Majalengka",
                callback_data="loc_majalengka"
            ),
            types.InlineKeyboardButton(
                "📍 Kuningan",
                callback_data="loc_kuningan"
            )
        )

        keyboard.add(
            types.InlineKeyboardButton(
                "🏠 Menu Utama",
                callback_data="menu"
            )
        )

        bot.edit_message_text(
            "📍 <b>Pilih lokasi pekerjaan:</b>",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
        )

    elif call.data == "kategori":
        keyboard = types.InlineKeyboardMarkup(row_width=2)

        keyboard.add(
            types.InlineKeyboardButton(
                "🏭 Operator",
                callback_data="cat_operator"
            ),
            types.InlineKeyboardButton(
                "📋 Admin",
                callback_data="cat_admin"
            )
        )

        keyboard.add(
            types.InlineKeyboardButton(
                "💰 Sales",
                callback_data="cat_sales"
            ),
            types.InlineKeyboardButton(
                "💻 IT",
                callback_data="cat_it"
            )
        )

        keyboard.add(
            types.InlineKeyboardButton(
                "🏠 Menu Utama",
                callback_data="menu"
            )
        )

        bot.edit_message_text(
            "💼 <b>Pilih kategori pekerjaan:</b>",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
        )

    elif call.data == "help":
        keyboard = types.InlineKeyboardMarkup()

        keyboard.add(
            types.InlineKeyboardButton(
                "🏠 Menu Utama",
                callback_data="menu"
            )
        )

        bot.edit_message_text(
            "ℹ️ <b>Pusat Bantuan</b>\n\n"
            "Gunakan menu untuk mencari informasi "
            "lowongan kerja terbaru.\n\n"
            "📢 @KerjaDimana_id",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
        )

    elif call.data.startswith("loc_"):
        lokasi_nama = call.data.replace(
            "loc_",
            ""
        ).title()

        bot.answer_callback_query(
            call.id,
            f"📍 Lokasi dipilih: {lokasi_nama}",
            show_alert=True
        )

    elif call.data.startswith("cat_"):
        kategori_nama = call.data.replace(
            "cat_",
            ""
        ).title()

        bot.answer_callback_query(
            call.id,
            f"💼 Kategori dipilih: {kategori_nama}",
            show_alert=True
        )


# =========================================================
# REGISTER COMMAND TELEGRAM
# =========================================================

bot.set_my_commands([
    types.BotCommand(
        "start",
        "Buka menu utama"
    ),
    types.BotCommand(
        "loker",
        "Lihat lowongan terbaru"
    ),
    types.BotCommand(
        "cari",
        "Cari lowongan kerja"
    ),
    types.BotCommand(
        "lokasi",
        "Cari berdasarkan lokasi"
    ),
    types.BotCommand(
        "kategori",
        "Cari berdasarkan kategori"
    ),
    types.BotCommand(
        "help",
        "Bantuan"
    )
])


# =========================================================
# PESAN TIDAK DIKENAL
# =========================================================

@bot.message_handler(
    func=lambda message: True,
    content_types=["text"]
)
def unknown(message):
    bot.send_message(
        message.chat.id,
        (
            "🤔 Saya belum memahami pesan tersebut.\n\n"
            "Ketik /start untuk membuka menu."
        ),
        reply_markup=main_menu()
    )


# =========================================================
# START BOT
# =========================================================

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 KerjaDimana.id Bot")
    print("✅ BOT AKTIF")
    print("=" * 50)

    bot.infinity_polling(
        skip_pending=True,
        timeout=30,
        long_polling_timeout=30
    )

