import json
from telegram import Update
from telegram.ext import ContextTypes
import config
import database.db_helper as db
from utils.keyboards import get_topics_keyboard, get_materi_nav_keyboard, get_video_nav_keyboard

def load_materials():
    with open(config.MATERIALS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

async def materi_menu_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📚 *MATERI PEMBELAJARAN INFORMATIKA*\n"
        "Elemen: *Jaringan Komputer dan Internet*\n\n"
        "Silakan pilih topik pembelajaran yang ingin Anda pelajari:"
    )
    await update.message.reply_text(
        text=text,
        reply_markup=get_topics_keyboard("materi"),
        parse_mode="Markdown"
    )

async def materi_topic_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data  # misal: materi_topik_1
    topic_id = int(data.split("_")[-1])

    materials_data = load_materials()
    topic = next((t for t in materials_data["topics"] if t["id"] == topic_id), None)

    if not topic:
        await query.edit_message_text("Topik materi belum tersedia.")
        return

    # Catat progres bahwa topik ini telah dibuka/dipelajari
    db.mark_topic_completed(query.from_user.id, topic_id)

    await query.message.reply_text(
        text=topic["content"],
        reply_markup=get_materi_nav_keyboard(topic_id),
        parse_mode="Markdown"
    )

async def video_menu_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🎬 *VIDEO PEMBELAJARAN*\n"
        "Silakan pilih topik yang ingin ditonton video pembelajarannya:"
    )
    await update.message.reply_text(
        text=text,
        reply_markup=get_topics_keyboard("video"),
        parse_mode="Markdown"
    )

async def video_topic_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    topic_id = int(query.data.split("_")[-1])
    materials_data = load_materials()
    topic = next((t for t in materials_data["topics"] if t["id"] == topic_id), None)

    if not topic:
        await query.edit_message_text("Video tidak ditemukan.")
        return

    db.mark_video_watched(query.from_user.id, topic_id)

    video_text = (
        f"🎬 *{topic['video_title']}*\n"
        f"⏱️ Durasi: `{topic['video_duration']}`\n\n"
        f"Tonton video penjelasan interaktif melalui tautan di bawah:\n"
        f"🔗 [Klik Di Sini Untuk Memutar Video]({topic['video_url']})\n\n"
        "_Setelah selesai menonton, Anda dapat kembali ke materi atau mengerjakan latihan soal._"
    )

    await query.message.reply_text(
        text=video_text,
        reply_markup=get_video_nav_keyboard(topic_id),
        parse_mode="Markdown",
        disable_web_page_preview=False
    )
