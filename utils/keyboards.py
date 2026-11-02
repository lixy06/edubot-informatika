from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu_keyboard():
    keyboard = [
        [KeyboardButton("📖 Materi Pembelajaran"), KeyboardButton("📝 Latihan Soal")],
        [KeyboardButton("🎬 Video Pembelajaran"), KeyboardButton("💬 Tanya Jawab")],
        [KeyboardButton("📊 Cek Progres"), KeyboardButton("👨‍💻 Profil Pengembang")],
        [KeyboardButton("❓ Bantuan")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_topics_keyboard(action_prefix="materi"):
    keyboard = [
        [InlineKeyboardButton("1. Mengenal Jaringan Komputer", callback_data=f"{action_prefix}_topik_1")],
        [InlineKeyboardButton("2. Mengkonfigurasi Perangkat Jaringan", callback_data=f"{action_prefix}_topik_2")],
        [InlineKeyboardButton("3. Mengoperasikan Perangkat Jaringan", callback_data=f"{action_prefix}_topik_3")],
        [InlineKeyboardButton("🔙 Menu Utama", callback_data="nav_main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_materi_nav_keyboard(topic_id: int):
    next_topic_id = topic_id + 1 if topic_id < 3 else 1
    keyboard = [
        [InlineKeyboardButton("🎬 Tonton Video Penjelasan", callback_data=f"video_topik_{topic_id}")],
        [InlineKeyboardButton("📝 Latihan Soal Topik Ini", callback_data=f"quiz_start_{topic_id}")],
        [InlineKeyboardButton(f"➡️ Topik Berikutnya ({next_topic_id})", callback_data=f"materi_topik_{next_topic_id}")],
        [InlineKeyboardButton("🏠 Menu Utama", callback_data="nav_main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_video_nav_keyboard(topic_id: int):
    keyboard = [
        [InlineKeyboardButton("📖 Kembali ke Materi", callback_data=f"materi_topik_{topic_id}")],
        [InlineKeyboardButton("🏠 Menu Utama", callback_data="nav_main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_quiz_options_keyboard(topic_id: int, q_idx: int, options: list):
    keyboard = []
    for opt in options:
        btn_text = f"{opt['key']}. {opt['text'][:35]}..." if len(opt['text']) > 35 else f"{opt['key']}. {opt['text']}"
        keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"qans_{topic_id}_{q_idx}_{opt['key']}")])
    return InlineKeyboardMarkup(keyboard)

def get_quiz_feedback_keyboard(topic_id: int, q_idx: int, is_correct: bool, has_next: bool):
    keyboard = []
    if not is_correct:
        keyboard.append([InlineKeyboardButton("🔄 Coba Lagi Soal Ini", callback_data=f"qretry_{topic_id}_{q_idx}")])
    
    if has_next:
        keyboard.append([InlineKeyboardButton("➡️ Soal Berikutnya", callback_data=f"qnext_{topic_id}_{q_idx + 1}")])
    else:
        keyboard.append([InlineKeyboardButton("🏆 Lihat Hasil Akhir", callback_data=f"qfinish_{topic_id}")])
        
    return InlineKeyboardMarkup(keyboard)

def get_quiz_result_keyboard(topic_id: int):
    keyboard = [
        [InlineKeyboardButton("📖 Baca Materi Lagi", callback_data=f"materi_topik_{topic_id}")],
        [InlineKeyboardButton("🔄 Ulangi Kuis", callback_data=f"quiz_start_{topic_id}")],
        [InlineKeyboardButton("🏠 Menu Utama", callback_data="nav_main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_faq_keyboard():
    keyboard = [
        [InlineKeyboardButton("Apa itu Jaringan Komputer?", callback_data="faq_q_jaringan")],
        [InlineKeyboardButton("Apa itu LAN?", callback_data="faq_q_lan")],
        [InlineKeyboardButton("Apa fungsi Router?", callback_data="faq_q_router")],
        [InlineKeyboardButton("Apa fungsi Switch?", callback_data="faq_q_switch")],
        [InlineKeyboardButton("Apa fungsi IP Address?", callback_data="faq_q_ip")],
        [InlineKeyboardButton("Bagaimana cara kerja Ping?", callback_data="faq_q_ping")],
        [InlineKeyboardButton("🏠 Menu Utama", callback_data="nav_main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_tanya_jawab_initial_keyboard():
    keyboard = [
        [InlineKeyboardButton("📋 Lihat Daftar Pertanyaan", callback_data="view_faq_list")],
        [InlineKeyboardButton("🏠 Menu Utama", callback_data="nav_main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_single_back_keyboard():
    keyboard = [
        [InlineKeyboardButton("🏠 Kembali ke Menu Utama", callback_data="nav_main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)
