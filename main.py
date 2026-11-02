import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

import config
from database.init_db import init_db

# Import Handlers
from handlers.start_handler import start_command, main_menu_callback
from handlers.materi_handler import (
    materi_menu_message,
    materi_topic_callback,
    video_menu_message,
    video_topic_callback
)
from handlers.quiz_handler import (
    quiz_menu_message,
    start_quiz_session,
    quiz_answer_callback,
    quiz_retry_callback,
    quiz_next_callback,
    quiz_finish_callback
)
from handlers.tanya_jawab_handler import (
    tanya_jawab_menu_message,
    view_faq_list_callback,
    faq_answer_callback,
    handle_user_text_question
)
from handlers.progres_handler import progres_menu_message
from handlers.info_handler import profile_menu_message, help_menu_message

def main():
    # 1. Inisialisasi Database
    init_db()

    # 2. Cek Token
    if not config.BOT_TOKEN or config.BOT_TOKEN == "ISI_DENGAN_TOKEN_BOT_TELEGRAM_ANDA":
        print("\n" + "="*70)
        print("PERINGATAN: BOT TOKEN BELUM DIISI!")
        print("Silakan buka file '.env' dan masukkan token bot dari @BotFather.")
        print("Contoh: TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxYZ")
        print("="*70 + "\n")
        return

    try:
        from telegram.ext import (
            ApplicationBuilder,
            CommandHandler,
            MessageHandler,
            CallbackQueryHandler,
            filters
        )
    except ImportError:
        print("\n[ERROR] Pustaka 'python-telegram-bot' belum terpasang.")
        print("Jalankan: pip install -r requirements.txt\n")
        return

    # 3. Bangun Aplikasi Bot
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    # --- Command Handlers ---
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("menu", start_command))
    app.add_handler(CommandHandler("materi", materi_menu_message))
    app.add_handler(CommandHandler("kuis", quiz_menu_message))
    app.add_handler(CommandHandler("progres", progres_menu_message))
    app.add_handler(CommandHandler("profil", profile_menu_message))
    app.add_handler(CommandHandler("bantuan", help_menu_message))
    app.add_handler(CommandHandler("help", help_menu_message))

    # --- Reply Keyboard Menu Handlers (Teks Tombol) ---
    app.add_handler(MessageHandler(filters.Regex("^📖 Materi Pembelajaran$"), materi_menu_message))
    app.add_handler(MessageHandler(filters.Regex("^📝 Latihan Soal$"), quiz_menu_message))
    app.add_handler(MessageHandler(filters.Regex("^🎬 Video Pembelajaran$"), video_menu_message))
    app.add_handler(MessageHandler(filters.Regex("^💬 Tanya Jawab$"), tanya_jawab_menu_message))
    app.add_handler(MessageHandler(filters.Regex("^📊 Cek Progres$"), progres_menu_message))
    app.add_handler(MessageHandler(filters.Regex("^👨‍💻 Profil Pengembang$"), profile_menu_message))
    app.add_handler(MessageHandler(filters.Regex("^❓ Bantuan$"), help_menu_message))

    # --- Callback Query Handlers (Inline Buttons) ---
    app.add_handler(CallbackQueryHandler(main_menu_callback, pattern="^nav_main_menu$"))
    
    # Materi & Video
    app.add_handler(CallbackQueryHandler(materi_topic_callback, pattern="^materi_topik_"))
    app.add_handler(CallbackQueryHandler(video_topic_callback, pattern="^video_topik_"))
    
    # Kuis
    app.add_handler(CallbackQueryHandler(start_quiz_session, pattern="^quiz_start_"))
    app.add_handler(CallbackQueryHandler(quiz_answer_callback, pattern="^qans_"))
    app.add_handler(CallbackQueryHandler(quiz_retry_callback, pattern="^qretry_"))
    app.add_handler(CallbackQueryHandler(quiz_next_callback, pattern="^qnext_"))
    app.add_handler(CallbackQueryHandler(quiz_finish_callback, pattern="^qfinish_"))

    # Tanya Jawab & FAQ
    app.add_handler(CallbackQueryHandler(view_faq_list_callback, pattern="^view_faq_list$"))
    app.add_handler(CallbackQueryHandler(faq_answer_callback, pattern="^faq_q_"))

    # --- Text Message Handler (Tanya Jawab Keyword Matcher) ---
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_text_question))

    print("\n[SUCCESS] EduBot Pembelajaran Informatika sedang berjalan...")
    print("Tekan Ctrl+C di terminal untuk menghentikan bot.\n")

    app.run_polling()

if __name__ == "__main__":
    main()
