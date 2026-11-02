from telegram import Update
from telegram.ext import ContextTypes
import database.db_helper as db
from utils.keyboards import get_main_menu_keyboard

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.register_student(
        telegram_id=user.id,
        username=user.username or "",
        full_name=user.full_name or "Siswa X TKJ"
    )

    welcome_text = (
        f"👋 *Halo, {user.first_name}!*\n"
        "Selamat datang di *EduBot – Media Pembelajaran Informatika* 🤖📚\n\n"
        "🎯 *Materi:* Jaringan Komputer dan Internet\n"
        "🏫 *Sasaran:* Siswa Kelas X TKJ – SMK 2 Telkom Medan\n"
        "📌 *Kurikulum:* Kurikulum Merdeka\n\n"
        "Gunakan menu interaktif di bawah ini untuk belajar materi secara mandiri, "
        "menonton video tutorial, mengerjakan kuis latihan, dan bertanya seputar materi."
    )

    await update.message.reply_text(
        text=welcome_text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="Markdown"
    )

async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    menu_text = (
        "🏠 *MENU UTAMA EDUBOT*\n\n"
        "Silakan pilih fitur yang ingin Anda akses melalui keyboard di bawah atau ketik pertanyaan langsung:"
    )

    await query.message.reply_text(
        text=menu_text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="Markdown"
    )
