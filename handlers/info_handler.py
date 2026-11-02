from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import get_single_back_keyboard

async def profile_menu_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👨‍💻 *PROFIL PENGEMBANG & PENELITIAN*\n\n"
        "🎓 *Identitas Peneliti:*\n"
        "• *Nama:* Dasminar Hutasoit\n"
        "• *NIM:* 5213351036\n"
        "• *Program Studi:* S-1 Pendidikan Teknologi Informatika dan Komputer (PTIK)\n"
        "• *Jurusan:* Pendidikan Teknik Elektro\n"
        "• *Fakultas / Universitas:* Fakultas Teknik, Universitas Negeri Medan (UNIMED)\n\n"
        "👨‍🏫 *Dosen Pembimbing Skripsi:*\n"
        "• Prof. Dr. Hamonangan Tambunan, S.T., M.Pd.\n\n"
        "🏫 *Lokasi Penelitian:*\n"
        "• SMK 2 Telkom Medan (Kelas X Jurusan TKJ)\n\n"
        "📖 *Judul Penelitian:*\n"
        "_\"Pengembangan Chatbot Sebagai Media Pembelajaran Berbasis Telegram Pada Mata Pelajaran Informatika Untuk Siswa Kelas X TKJ Di SMK 2 Telkom Medan\"_\n\n"
        "Tahun Pengembangan: 2026/2027"
    )
    await update.message.reply_text(
        text=text,
        reply_markup=get_single_back_keyboard(),
        parse_mode="Markdown"
    )

async def help_menu_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "❓ *PUSAT BANTUAN & PANDUAN PENGGUNAAN*\n\n"
        "🤖 *Tentang EduBot:*\n"
        "EduBot adalah media pembelajaran berbantuan komputer (*CAI*) yang memfasilitasi Anda belajar mandiri materi Informatika.\n\n"
        "📌 *Cara Menggunakan:*\n"
        "1. *Membaca Materi:* Tekan tombol `📖 Materi Pembelajaran` lalu pilih topik yang ingin dipelajari.\n"
        "2. *Menonton Video:* Tekan tombol `🎬 Video Pembelajaran` untuk melihat video peragaan.\n"
        "3. *Latihan Kuis:* Tekan tombol `📝 Latihan Soal` untuk menguji pemahaman. Kuis dilengkapi pembahasan langsung!\n"
        "4. *Tanya Jawab:* Ketik pertanyaan Anda di chat (contoh: _\"apa itu router\"_), bot akan menjawab secara otomatis.\n"
        "5. *Cek Nilai:* Tekan tombol `📊 Cek Progres` untuk memantau capaian belajar Anda.\n\n"
        "⌨️ *Daftar Perintah Cepat (Slash Commands):*\n"
        "• `/start` : Memulai ulang bot & membuka menu utama\n"
        "• `/materi` : Membuka daftar modul pembelajaran\n"
        "• `/kuis`   : Memulai latihan soal interaktif\n"
        "• `/progres`: Melihat status dan nilai kuis\n"
        "• `/profil` : Menampilkan informasi peneliti\n"
        "• `/bantuan`: Menampilkan pesan panduan ini\n\n"
        "Jika bot tidak merespons, kirim perintah `/start` untuk menyegarkan sesi."
    )
    await update.message.reply_text(
        text=text,
        reply_markup=get_single_back_keyboard(),
        parse_mode="Markdown"
    )
