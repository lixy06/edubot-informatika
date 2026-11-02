import json
from telegram import Update
from telegram.ext import ContextTypes
import config
import database.db_helper as db
from utils.keyboards import (
    get_topics_keyboard,
    get_quiz_options_keyboard,
    get_quiz_feedback_keyboard,
    get_quiz_result_keyboard
)

def load_quiz_bank():
    with open(config.QUIZ_BANK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

async def quiz_menu_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📝 *LATIHAN SOAL & KUIS INFORMATIKA*\n\n"
        "Pilih topik kuis yang ingin Anda kerjakan:\n"
        "Setiap soal dilengkapi penilaian langsung dan pembahasan lengkap!"
    )
    await update.message.reply_text(
        text=text,
        reply_markup=get_topics_keyboard("quiz_start"),
        parse_mode="Markdown"
    )

async def start_quiz_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    topic_id = int(query.data.split("_")[-1])
    bank = load_quiz_bank()
    key = f"topik_{topic_id}"
    questions = bank.get(key, [])

    if not questions:
        await query.message.reply_text(f"⚠️ Soal untuk Topik {topic_id} sedang disiapkan.")
        return

    # Inisialisasi sesi kuis pengguna
    context.user_data["quiz"] = {
        "topic_id": topic_id,
        "questions": questions,
        "current_index": 0,
        "correct_count": 0,
        "total_questions": len(questions),
        "history": []
    }

    await send_quiz_question(query, context)

async def send_quiz_question(query, context: ContextTypes.DEFAULT_TYPE):
    q_data = context.user_data.get("quiz")
    idx = q_data["current_index"]
    questions = q_data["questions"]
    q = questions[idx]

    text = (
        f"📝 *SOAL {idx + 1} dari {len(questions)}* (Topik {q_data['topic_id']})\n\n"
        f"{q['question']}\n\n"
        "_Pilih salah satu jawaban di bawah:_"
    )

    await query.message.reply_text(
        text=text,
        reply_markup=get_quiz_options_keyboard(q_data["topic_id"], idx, q["options"]),
        parse_mode="Markdown"
    )

async def quiz_answer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    parts = query.data.split("_")  # qans_{topic_id}_{idx}_{selected_key}
    topic_id = int(parts[1])
    idx = int(parts[2])
    selected_key = parts[3]

    q_data = context.user_data.get("quiz")
    if not q_data or q_data["current_index"] != idx:
        await query.edit_message_text("Sesi kuis telah usai atau tidak valid. Silakan mulai kembali.")
        return

    q = q_data["questions"][idx]
    is_correct = (selected_key == q["correct"])

    if is_correct:
        q_data["correct_count"] += 1
        feedback_text = (
            f"✅ *JAWABAN BENAR!*\n\n"
            f"Pilihan Anda: *{selected_key}*\n"
            f"💡 *Penjelasan:* {q['explanation']}\n\n"
            f"Skor sementara: `{q_data['correct_count']}/{idx + 1}`"
        )
    else:
        feedback_text = (
            f"❌ *KURANG TEPAT!*\n\n"
            f"Jawaban Anda: *{selected_key}*\n"
            f"Kunci Jawaban Benar: *{q['correct']}*\n\n"
            f"💡 *Penjelasan:* {q['explanation']}\n\n"
            f"Skor sementara: `{q_data['correct_count']}/{idx + 1}`"
        )

    has_next = (idx + 1 < q_data["total_questions"])

    await query.edit_message_text(
        text=feedback_text,
        reply_markup=get_quiz_feedback_keyboard(topic_id, idx, is_correct, has_next),
        parse_mode="Markdown"
    )

async def quiz_retry_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await send_quiz_question(query, context)

async def quiz_next_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    q_data = context.user_data.get("quiz")
    if q_data:
        q_data["current_index"] += 1
        await send_quiz_question(query, context)

async def quiz_finish_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    q_data = context.user_data.get("quiz")
    if not q_data:
        await query.message.reply_text("Data kuis tidak ditemukan.")
        return

    total = q_data["total_questions"]
    correct = q_data["correct_count"]
    score = round((correct / total) * 100, 1)
    topic_id = q_data["topic_id"]

    # Simpan hasil kuis ke database SQLite
    db.save_quiz_attempt(query.from_user.id, topic_id, total, correct, score)

    if score >= 80:
        predikat = "🏆 *SANGAT BAIK (TUNTAS)*"
        rekomendasi = "Hebat! Anda telah menguasai kompetensi dasar topik ini dengan sangat baik."
    elif score >= 60:
        predikat = "👍 *CUKUP (TUNTAS BERSYARAT)*"
        rekomendasi = "Bagus! Silakan baca ulang beberapa poin konsep yang keliru agar makin mantap."
    else:
        predikat = "⚠️ *PERLU BELAJAR LAGI*"
        rekomendasi = "Jangan berkecil hati! Pelajari kembali materi modul sebelum mengulangi kuis."

    result_text = (
        f"🏆 *HASIL AKHIR KUIS - TOPIK {topic_id}*\n\n"
        f"📊 Skor Akhir: *{score} / 100* ({score}%)\n"
        f"✅ Jawaban Benar: *{correct}*\n"
        f"❌ Jawaban Salah: *{total - correct}*\n"
        f"🎖️ Status: {predikat}\n\n"
        f"💡 *Rekomendasi Belajar:*\n{rekomendasi}"
    )

    await query.message.reply_text(
        text=result_text,
        reply_markup=get_quiz_result_keyboard(topic_id),
        parse_mode="Markdown"
    )
