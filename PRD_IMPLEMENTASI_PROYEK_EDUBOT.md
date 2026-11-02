# DOKUMEN IMPLEMENTASI TEKNIS & BLUEPRINT PROYEK
# EduBot – Media Pembelajaran Informatika Berbasis Bot Telegram

**Mata Pelajaran:** Informatika (Jaringan Komputer dan Internet)  
**Sasaran Pengguna:** Siswa Kelas X TKJ SMK 2 Telkom Medan  
**Peneliti:** Dasminar Hutasoit (NIM: 5213351036) – PTIK FT UNIMED  
**Dosen Pembimbing:** Prof. Dr. Hamonangan Tambunan, S.T., M.Pd.  
**Status Proyek:** Siap Dijalankan (*Ready-to-Run Scaffolding Completed*)

---

## 1. STRUKTUR LENGKAP PROYEK YANG TELAH DIBUAT

```
c:\xampp\htdocs\EduBotTELE - Media Pembelajaran Informatika\
│
├── .env.example                  # Template konfigurasi token bot
├── .env                          # File konfigurasi utama (tempat menaruh BOT TOKEN)
├── config.py                     # Pemetaan path dan loader environment variable
├── requirements.txt              # Daftar pustaka Python (python-telegram-bot, python-dotenv)
├── main.py                       # Entry point aplikasi bot & pendaftaran handler
│
├── data/                         # Direktori penyimpanan berkas konten hibrida
│   ├── materials.json            # Konten materi Topik 1, 2, dan 3 + link video
│   ├── quiz_bank.json            # Bank soal kuis pilihan ganda + kunci + pembahasan
│   └── knowledge_base.json       # Basis pengetahuan tanya jawab terkontrol (FAQ & Fallback)
│
├── database/                     # Direktori basis data SQLite lokal
│   ├── init_db.py                # Skrip pembuat tabel database
│   ├── db_helper.py              # Fungsi query SQLite (CRUD siswa, progres, nilai kuis)
│   └── edubot_database.sqlite    # File database SQLite aktif
│
├── handlers/                     # Modul pengendali alur percakapan (Controllers)
│   ├── start_handler.py          # Handler /start & menu utama (Scene 1 & 2)
│   ├── materi_handler.py         # Handler modul materi & video (Scene 3, 4, 5)
│   ├── quiz_handler.py           # Handler kuis interaktif & umpan balik (Scene 6, 7, 8)
│   ├── tanya_jawab_handler.py    # Handler tanya jawab & pencocokan kata kunci (Scene 9-12)
│   ├── progres_handler.py        # Handler visualisasi progres belajar (Scene 13)
│   └── info_handler.py           # Handler profil peneliti & pusat bantuan (Scene 14 & 15)
│
└── utils/                        # Komponen utilitas antarmuka
    └── keyboards.py              # Generator Reply Keyboard & Inline Keyboard 15 Scene
```

---

## 2. LANGKAH-LANGKAH AKTIVASI CEPAT (LANGSUNG JALAN)

### Langkah 1: Dapatkan Token Bot dari @BotFather
1. Buka aplikasi Telegram di HP atau Laptop Anda.
2. Cari akun resmi Telegram: **`@BotFather`**.
3. Ketik perintah `/newbot` dan ikuti instruksi:
   * Masukkan nama bot: misal `EduBot Informatika SMK Telkom`
   * Masukkan username bot: misal `EduBotInformatika_bot` (harus berakhiran `bot`).
4. `@BotFather` akan memberikan **HTTP API Token**, contohnya:
   `7123456789:AAFlm39cKabcdefghijk1234567890`

### Langkah 2: Salin Token ke Berkas `.env`
Buka file `.env` di folder proyek ini, lalu ubah baris:
```ini
TELEGRAM_BOT_TOKEN=7123456789:AAFlm39cKabcdefghijk1234567890
```
*(Ganti dengan token asli dari BotFather)*

### Langkah 3: Jalankan Bot di Terminal
Buka terminal PowerShell pada direktori ini, kemudian ketik:
```powershell
python main.py
```

Jika berhasil, terminal akan menampilkan pesan:
```
[SUCCESS] Database SQLite berhasil diinisialisasi di: .../database/edubot_database.sqlite
[SUCCESS] EduBot Pembelajaran Informatika sedang berjalan...
Tekan Ctrl+C di terminal untuk menghentikan bot.
```

### Langkah 4: Uji Coba di Telegram
1. Buka Telegram dan cari username bot Anda (misal `@EduBotInformatika_bot`).
2. Tekan tombol **START** atau kirim pesan `/start`.
3. Seluruh 7 tombol menu utama akan muncul dan siap digunakan.

---

## 3. PEMETAAN FITUR & SCENE TERHADAP KODE PROGRAM

| Scene Proposal | Fungsi Fitur | File Handler Pengendali | Komponen Keyboard |
| :---: | :--- | :--- | :--- |
| **Scene 1 & 2** | Start & Menu Utama | `handlers/start_handler.py` | `get_main_menu_keyboard()` |
| **Scene 3** | Daftar Materi | `handlers/materi_handler.py` | `get_topics_keyboard()` |
| **Scene 4** | Konten Materi Teks | `handlers/materi_handler.py` | `get_materi_nav_keyboard()` |
| **Scene 5** | Video Edukasi | `handlers/materi_handler.py` | `get_video_nav_keyboard()` |
| **Scene 6** | Soal Kuis Pilihan Ganda | `handlers/quiz_handler.py` | `get_quiz_options_keyboard()` |
| **Scene 7** | Umpan Balik Instan | `handlers/quiz_handler.py` | `get_quiz_feedback_keyboard()` |
| **Scene 8** | Kartu Hasil Akhir Kuis | `handlers/quiz_handler.py` | `get_quiz_result_keyboard()` |
| **Scene 9 - 12** | Tanya Jawab & FAQ | `handlers/tanya_jawab_handler.py` | `get_faq_keyboard()` |
| **Scene 13** | Cek Progres Belajar | `handlers/progres_handler.py` | Visual Progress Bar Text |
| **Scene 14** | Profil Pengembang | `handlers/info_handler.py` | Data Dasminar Hutasoit / UNIMED |
| **Scene 15** | Bantuan & Perintah | `handlers/info_handler.py` | Daftar Slash Commands |

---

## 4. PEMELIHARAAN & PENAMBAHAN KONTEN

* **Menambah atau Mengedit Materi:** Cukup buka berkas [`data/materials.json`](file:///c:/xampp/htdocs/EduBotTELE%20-%20Media%20Pembelajaran%20Informatika/data/materials.json) dan sesuaikan teks atau link video YouTube.
* **Menambah Soal Kuis:** Buka berkas [`data/quiz_bank.json`](file:///c:/xampp/htdocs/EduBotTELE%20-%20Media%20Pembelajaran%20Informatika/data/quiz_bank.json) lalu tambahkan objek pertanyaan baru beserta opsi A–D, kunci jawaban, dan pembahasannya.
* **Menambah Respon Tanya Jawab:** Buka berkas [`data/knowledge_base.json`](file:///c:/xampp/htdocs/EduBotTELE%20-%20Media%20Pembelajaran%20Informatika/data/knowledge_base.json) lalu tambahkan variasi kata kunci (*keywords*) dan jawabannya.
