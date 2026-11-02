from telegram import Update
from telegram.ext import ContextTypes
import database.db_helper as db
from utils.keyboards import get_single_back_keyboard

async def progres_menu_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    stats = db.get_student_stats(user.id)

    total_topics = 3
    completed = stats["completed_count"]
    percentage = int((completed / total_topics) * 100)

    # Progress bar visual 10 karakter
    filled_len = int(percentage / 10)
    bar = "█" * filled_len + "░" * (10 - filled_len)

    topik_status = []
    topik_names = [
        (1, "Mengenal Jaringan Komputer"),
        (2, "Mengkonfigurasi Perangkat Jaringan"),
        (3, "Mengoperasikan Perangkat Jaringan")
    ]

    for tid, name in topik_names:
        mark = "✅" if tid in stats["completed_topics"] else "⏳"
        topik_status.append(f"{mark} Topik {tid}: *{name}*")

    status_str = "\n".join(topik_status)

    if completed == 3 and stats["avg_score"] >= 80:
        saran = "🎉 *Selamat!* Anda telah menyelesaikan semua modul dengan predikat memuaskan."
    elif completed < 3:
        next_t = next((tid for tid, _ in topik_names if tid not in stats["completed_topics"]), 1)
        saran = f"📌 *Saran Belajar:* Lanjutkan dengan membaca materi *Topik {next_t}* ya!"
    else:
        saran = "💡 *Saran Belajar:* Anda telah membaca semua materi. Tingkatkan skor kuis Anda agar lebih optimal!"

    text = (
        f"📊 *PROGRES BELAJAR SAYA*\n\n"
        f"👤 *Nama:* {user.full_name}\n"
        f"🏫 *Kelas:* X TKJ (SMK 2 Telkom Medan)\n\n"
        f"📈 *Status Materi:* `{completed}/{total_topics}` Topik Tuntas\n"
        f"Progress: `[{bar}] {percentage}%`\n\n"
        f"📑 *Daftar Topik Pembelajaran:*\n{status_str}\n\n"
        f"📝 *Evaluasi Kuis:*\n"
        f"• Total Percobaan Kuis: `{stats['quiz_count']}` kali\n"
        f"• Rata-rata Skor: `{stats['avg_score']}` / 100\n\n"
        f"{saran}"
    )

    await update.message.reply_text(
        text=text,
        reply_markup=get_single_back_keyboard(),
        parse_mode="Markdown"
    )
