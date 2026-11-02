import json
import re
from telegram import Update
from telegram.ext import ContextTypes
import config
from utils.keyboards import (
    get_tanya_jawab_initial_keyboard,
    get_faq_keyboard,
    get_single_back_keyboard
)

def load_kb():
    with open(config.KNOWLEDGE_BASE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

async def tanya_jawab_menu_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💬 *FITUR TANYA JAWAB EDUKATIF*\n\n"
        "Anda dapat menanyakan konsep seputar materi *Jaringan Komputer dan Internet*.\n\n"
        "💡 *Contoh pertanyaan:*\n"
        "• _Apa itu jaringan komputer?_\n"
        "• _Apa fungsi router?_\n"
        "• _Apa itu LAN?_\n"
        "• _Apa kegunaan IP Address?_\n"
        "• _Bagaimana cara kerja ping?_\n\n"
        "Ketik pertanyaan Anda langsung di kolom obrolan ini, atau tekan tombol di bawah untuk melihat daftar pertanyaan populer:"
    )
    await update.message.reply_text(
        text=text,
        reply_markup=get_tanya_jawab_initial_keyboard(),
        parse_mode="Markdown"
    )

async def view_faq_list_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = (
        "📋 *DAFTAR PERTANYAAN CEPAT (FAQ)*\n\n"
        "Pilih salah satu pertanyaan umum di bawah untuk melihat penjelasannya langsung:"
    )
    await query.message.reply_text(
        text=text,
        reply_markup=get_faq_keyboard(),
        parse_mode="Markdown"
    )

async def faq_answer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    kb = load_kb()
    data = query.data

    intent_map = {
        "faq_q_jaringan": "pengertian_jaringan",
        "faq_q_lan": "pengertian_lan",
        "faq_q_router": "fungsi_router",
        "faq_q_switch": "fungsi_switch",
        "faq_q_ip": "fungsi_ip_address",
        "faq_q_ping": "cara_kerja_ping"
    }

    target_intent = intent_map.get(data, "")
    entry = next((item for item in kb["faq"] if item["intent"] == target_intent), None)

    if entry:
        resp = f"{entry['answer']}\n\n🏷️ _Terkait: {entry['related_topic']}_"
    else:
        resp = kb["fallback_response"]

    await query.message.reply_text(
        text=resp,
        reply_markup=get_single_back_keyboard(),
        parse_mode="Markdown"
    )

async def handle_user_text_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip().lower()

    # Cek apakah teks adalah salah satu menu utama tombol reply
    menu_buttons = [
        "📖 materi pembelajaran", "📝 latihan soal", "🎬 video pembelajaran",
        "💬 tanya jawab", "📊 cek progres", "👨‍💻 profil pengembang", "❓ bantuan"
    ]
    if user_text in menu_buttons:
        return

    kb = load_kb()
    matched_entry = None

    # Pencocokan kata kunci berbasis aturan (Rule-based Keyword Matching)
    for entry in kb["faq"]:
        for kw in entry["keywords"]:
            if kw in user_text:
                matched_entry = entry
                break
        if matched_entry:
            break

    if matched_entry:
        resp = (
            f"{matched_entry['answer']}\n\n"
            f"🏷️ *Rujukan Materi:* `{matched_entry['related_topic']}`\n\n"
            "_Ketik pertanyaan lain atau gunakan menu navigasi untuk melanjutkan belajar._"
        )
        await update.message.reply_text(
            text=resp,
            reply_markup=get_tanya_jawab_initial_keyboard(),
            parse_mode="Markdown"
        )
    else:
        # Fallback response jika di luar cakupan materi kurikulum
        await update.message.reply_text(
            text=kb["fallback_response"],
            reply_markup=get_faq_keyboard(),
            parse_mode="Markdown"
        )
