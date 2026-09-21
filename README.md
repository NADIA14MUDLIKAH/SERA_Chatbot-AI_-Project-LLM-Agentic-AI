# SERA (Sistem Edukasi & Rekomendasi Agrikultur)

Repositori ini memuat kode sumber dari proyek SERA, sebuah chatbot AI yang dibangun untuk memenuhi tugas perkuliahan terkait implementasi *Large Language Model* (LLM) menggunakan API pihak ketiga.

## 1. Latar Belakang & Konsep Utama

**Tema:** Asisten Konsultasi Pertanian (Identifikasi Gejala, Penyakit, dan Perawatan Tanaman)

**Konsep:**
Petani sering kali tidak mengetahui nama penyakit atau hama yang menyerang tanamannya. Mereka umumnya hanya bisa menceritakan gejala yang terlihat, seperti "daun menguning", "daun keriting", atau "tanaman layu mendadak". Berbeda dengan chatbot pada umumnya yang langsung menebak penyakit hanya dari satu kalimat keluhan, SERA dirancang menggunakan metode **konsultasi bertahap**. Sistem akan bertindak layaknya penyuluh pertanian sungguhan yang menanyakan kondisi pendukung (seperti intensitas penyiraman, cuaca, atau keberadaan hama) secara dua arah. Setelah informasi dirasa cukup, barulah chatbot memberikan diagnosa dan saran perawatan yang tepat.

**Cakupan Tanaman:**
SERA memiliki data khusus untuk tanaman **cabai, tomat, padi, dan jagung**. Untuk tanaman lain (misalnya terong atau kentang), SERA menggunakan panduan umum dan akan menyampaikan bahwa jawaban tersebut bersifat umum.

**Batasan Sistem:**
- SERA hanya menjawab pertanyaan seputar pertanian dan akan menolak topik di luar itu dengan sopan.
- Jawaban SERA berupa **kemungkinan penyebab**, bukan diagnosa pasti, karena sistem tidak dapat melihat kondisi tanaman secara langsung.
- Untuk kasus yang berat atau menyebar luas, SERA akan menyarankan pengguna menghubungi penyuluh pertanian lapangan (PPL) atau Dinas Pertanian setempat.

## 2. Cara Menjalankan Program

**Persiapan Awal:**
Pastikan komputer yang digunakan sudah terinstal Python (minimal versi 3.9, proyek ini dikembangkan menggunakan Python 3.11) dan terhubung ke internet.

**Langkah 1: Mengunduh Repositori**
Unduh atau *clone* proyek ini ke dalam penyimpanan komputer melalui terminal:
```bash
git clone <link-repositori-github-milikmu>
cd SERA_Project
```

**Langkah 2: Membuat Virtual Environment**
Sangat disarankan untuk membuat virtual environment agar proses instalasi modul proyek ini tidak mengganggu sistem bawaan laptop:

- **Windows:** Ketik `python -m venv venv` lalu aktifkan dengan `venv\Scripts\activate`
- **Mac/Linux:** Ketik `python3 -m venv venv` lalu aktifkan dengan `source venv/bin/activate`

**Langkah 3: Instalasi Modul Pendukung**
Instal seluruh library yang dibutuhkan (seperti `groq` dan `streamlit`) dengan menjalankan perintah:
```bash
pip install -r requirements.txt
```

**Langkah 4: Pengaturan API Key**
Aplikasi ini membutuhkan kunci rahasia (API Key) dari Groq agar bisa beroperasi.

1. Buat file teks baru bernama `.env` di dalam folder utama proyek (sejajar dengan file README ini).
2. Masukkan API Key tersebut ke dalam file dengan format penulisan seperti ini:
```env
GROQ_API_KEY=masukkan_api_key_disini
```

*(Catatan: File `.env` ini sudah dikecualikan oleh aturan `.gitignore`, sehingga aman dan kodenya tidak akan bocor saat diunggah ke GitHub).*

*(Catatan: Akun gratis Groq memiliki batas jumlah token per menit. Jika muncul pesan galat "rate limit", tunggu sekitar satu menit lalu kirim ulang pesan Anda).*

**Langkah 5: Menjalankan Aplikasi**
Proyek ini menyediakan dua pilihan tampilan yang bisa digunakan:

**Tampilan Terminal (CLI):**
Jalankan program secara sederhana di terminal dengan mengetikkan:
```bash
python -m src.main
```
Pada mode ini, pengguna bisa mengetik `clear` untuk mereset obrolan dari awal, `save` untuk menyimpan teks percakapan, atau `exit` untuk menutup aplikasi.

**Tampilan Web (Streamlit):**
Untuk membuka antarmuka visual yang lebih interaktif di browser, gunakan perintah:
```bash
python -m streamlit run streamlit/app.py
```
Setelah dijalankan, aplikasi dapat dibuka melalui alamat `http://localhost:8501`. Disarankan menggunakan browser versi terbaru (Chrome atau Edge) agar seluruh tampilan dapat dirender dengan baik.

## 3. Cuplikan Layar (Screenshots)

Berikut adalah dokumentasi visual saat sistem merespons keluhan dan mengingat konteks percakapan sebelumnya:

**Interaksi di Terminal:**

![Interaksi di Terminal]
![alt text](<Screenshoot/ss_terminal 1.png>)
![alt text](<Screenshoot/ss_terminal 2.png>)

*Gambar di atas merupakan tampilan SERA pada terminal. Sistem tidak langsung mendiagnosa, tetapi terlebih dahulu menanyakan kondisi pendukung kepada pengguna.*

**Antarmuka Web (Streamlit):**

![Antarmuka Web] 
![alt text](<Screenshoot/ss_web 1.png>)
![alt text](<Screenshoot/ss_web 2.png>)
![alt text](<Screenshoot/ss_web 3.png>)
![alt text](<Screenshoot/ss_web 4.png>)
![alt text](<Screenshoot/ss_web 5.png>)
![alt text](<Screenshoot/ss_web 6.png>)
*Gambar di atas merupakan tampilan SERA pada web. Bagian kiri memuat panel kontrol (ide cepat, cara kerja, simpan riwayat, dan percakapan baru), sedangkan bagian tengah memuat area percakapan dalam bentuk chat bubble.*

## 3. Contoh Alur Percakapan

Berikut adalah cuplikan interaksi asli dari sistem SERA yang menunjukkan bagaimana fitur **konsultasi bertahap**, **penolakan halus (pembatasan AI)**, dan **perintah khusus** (simpan/hapus riwayat) bekerja dengan baik.

### Contoh 1 - Konsultasi via Web (Kasus Tanaman Cabai)
Pada contoh ini, sistem memandu pengguna mengidentifikasi gejala keriting daun, memberikan estimasi, hingga menyusun panduan teknis penyemprotan.

> **🧑‍🌾 Pengguna:** Halo Sera, Daun cabe saya keriting nih.
> 
> **🤖 SERA:** Halo, maaf mendengar daun cabai Anda keriting. 😔 Untuk memperjelas penyebabnya, boleh saya tahu:
> 1. Apakah Anda melihat serangga kecil seperti kutu atau tungau di bagian bawah daun?
> 2. Apakah daun melengkung ke atas atau justru melengkung ke bawah?
>
> **🧑‍🌾 Pengguna:** Daunnya ada kutu kecil, melengkung ke bawah.
>
> **🤖 SERA:** **Kemungkinan Penyebab:** Serangan kutu daun (atau aphids) pada cabai... *(Sistem melampirkan Saran Perawatan dan Pencegahan).*
>
> **🧑‍🌾 Pengguna:** Kalo pake pestisida, jenis dan merknya apa ya sama estimasi harganya berapa?
> 
> **🤖 SERA:** Untuk mengendalikan kutu daun pada cabai, pilihan yang paling aman dan ramah lingkungan adalah pestisida nabati, contohnya ekstrak mimba (neem oil).
> **Estimasi harga:** Produk neem oil biasanya dijual dalam botol 100 ml - 250 ml dengan harga sekitar Rp 30.000 - Rp 80.000...
>
> **🧑‍🌾 Pengguna:** Saya mau panduan penggunaan pestisida tersebut.
>
> **🤖 SERA:** Berikut panduan singkat penggunaan ekstrak mimba (neem oil):
> 1. Persiapan larutan
> 2. Waktu penyemprotan
> 3. Cara penyemprotan... *(dan seterusnya hingga panduan pasca-penyemprotan).*

---

### Contoh 2 - Konsultasi via Terminal CLI (Kasus Tanaman Terong)
Pada contoh ini, AI menunjukkan kemampuannya menjaga batasan (*guardrails*) dengan menolak memberikan harga/merk pestisida spesifik di luar pengetahuannya, lalu diakhiri dengan eksekusi perintah khusus oleh pengguna.

> **🧑‍🌾 Petani:** Halo SERA daun terong saya kuning-kuning nih.
>
> **🤖 SERA:** Halo, terima kasih sudah menghubungi saya 🌱. Untuk membantu mengetahui penyebabnya, boleh saya tahu:
> - Tanah di sekitar terong Anda biasanya basah/berair atau justru kering?
> - Daun yang menguning duluan, apakah daun tua di bagian bawah atau daun muda di pucuk?
>
> **🧑‍🌾 Petani:** Daun bawah, tanahnya biasa aja.
>
> **🤖 SERA:** Kemungkinan penyebabnya cukup tinggi terkait kekurangan unsur hara pada terong Anda, karena daun tua di bagian bawah yang menguning biasanya menandakan tanaman kurang nutrisi (misalnya nitrogen, magnesium, atau besi)... *(Sistem melampirkan saran pemupukan).*
>
> **🧑‍🌾 Petani:** Ada rekomendasi penggunaan pestisida ngga, kalo ada kasi estimasi harga pestisidanya ya.
>
> **🤖 SERA:** Maaf, saya tidak dapat memberikan rekomendasi merek atau perkiraan harga pestisida secara spesifik. Jika Anda curiga ada serangan hama, berikut langkah aman yang dapat dicoba terlebih dahulu: Pengendalian nabati (minyak neem), Pengendalian mekanik, dan Sanitasi lahan...
>
> **🧑‍🌾 Petani:** save
> **🤖 SERA:** 💾 Percakapan berhasil disimpan di: `history\chat_20260921_192744.json`
>
> **🧑‍🌾 Petani:** clear
> **🤖 SERA:** ✅ Riwayat percakapan telah dibersihkan.
> 
> **🧑‍🌾 Petani:** exit
> **🤖 SERA:** Terima kasih telah menggunakan SERA. Sampai jumpa!

## 4. Penjelasan Struktur Kode

Proyek ini dibangun menggunakan arsitektur modular (*Separation of Concerns*) agar logika kerjanya rapi, mudah dilacak, dan gampang dikembangkan lebih lanjut. Berikut adalah hierarki lengkap direktori proyek SERA:

```text
SERA_Project/
├── data/
│   └── knowledge_base.json
├── history/
├── src/
│   ├── __init__.py
│   ├── chatbot.py
│   ├── commands.py
│   ├── config.py
│   ├── conversation.py
│   ├── knowledge_base.py
│   ├── llm_client.py
│   ├── main.py
│   └── prompts.py
├── streamlit/
│   └── app.py
├── tests/
│   └── test_chatbot.py
├── venv/
├── .env
├── .gitignore
├── logo.jpg
├── README.md
└── requirements.txt

- **`data/knowledge_base.json`**: File statis berisi data-data pertanian yang menjadi acuan dasar bagi AI agar jawabannya tetap sesuai fakta. Data dikelompokkan per tanaman (cabai, tomat, padi, jagung, dan panduan umum) dan setiap kasus memuat gejala utama, sinonim gejala dalam bahasa sehari-hari, pertanyaan lanjutan, kondisi pendukung, kemungkinan penyebab, ciri pembeda, saran perawatan, pencegahan, dan tingkat urgensi.
- **`src/config.py`**: File pengaturan untuk menentukan model AI yang dipakai (`openai/gpt-oss-120b`) dan mengatur agar jawabannya tidak terlalu melenceng.
- **`src/prompts.py`**: File khusus untuk menyimpan kerangka instruksi (*system prompt*). Isinya mengatur alur konsultasi bertahap, melarang chatbot memberikan diagnosa pada keluhan pertama, membatasi jumlah pertanyaan dalam satu balasan, memuat aturan keamanan penggunaan pestisida, serta melarang chatbot menjawab pertanyaan di luar konteks pertanian.
- **`src/knowledge_base.py`**: Modul yang membaca `knowledge_base.json` dan memilih hanya kasus yang paling sesuai dengan percakapan (berdasarkan jenis tanaman dan gejala yang disebutkan pengguna). Cara ini dipilih agar jumlah token yang dikirim ke API tetap kecil dan tidak melampaui batas akun gratis.
- **`src/conversation.py`**: Modul yang bertugas menyimpan riwayat obrolan secara berurutan, sehingga sistem tetap mengingat topik pembicaraan dari awal sampai akhir. Modul ini juga memperbarui isi *system prompt* pada setiap giliran sesuai gejala yang sedang dibahas dan membatasi riwayat yang dikirim ke model pada pesan-pesan terbaru saja.
- **`src/llm_client.py`**: Modul penghubung ke server Groq API yang sudah dilengkapi sistem penanganan masalah, sehingga jika koneksi internet terputus, program tidak akan langsung tertutup paksa (*crash*).
- **`src/commands.py`**: Modul yang menangani perintah khusus, termasuk penyimpanan transkrip percakapan ke dalam file.
- **`src/chatbot.py`**: Modul pusat penggerak yang mengatur jalannya obrolan, mulai dari menerima pesan, menyimpan riwayat, hingga merespons perintah khusus. Jika permintaan ke API gagal, pesan galat tidak disimpan sebagai jawaban sehingga pengguna dapat mengirim ulang pesannya.
- **`src/main.py`**: File utama yang dieksekusi jika ingin menjalankan program melalui terminal.
- **`streamlit/app.py`**: File yang digunakan untuk menjalankan antarmuka web visual bergaya chat bubble modern dengan warna yang disesuaikan dengan logo SERA. Pada bagian samping kiri tampilan ini terdapat panel kontrol yang memuat logo, ringkasan sesi, tombol **Ide Cepat** (contoh keluhan yang bisa langsung dikirim, misalnya daun menguning atau tanaman layu), panduan **Cara Kerja SERA**, tombol **Simpan Riwayat** untuk menyimpan transkrip konsultasi, dan tombol **Percakapan Baru** untuk mengosongkan layar obrolan dari awal. Pada bagian tengah, pengguna dapat menceritakan gejala tanamannya agar sistem dapat memandu proses identifikasi secara bertahap.

## 5. Pemanfaatan AI dalam Pengerjaan

Dalam pengerjaan proyek ini, penulis memanfaatkan asisten AI (Claude dari Anthropic) pada beberapa bagian. Berikut pembagian antara bagian yang dibantu AI dan bagian yang dikerjakan secara mandiri.

**Bagian yang dibantu AI:**

| Bagian | Bentuk Bantuan AI |
|---|---|
| `streamlit/app.py` | Perancangan ulang tampilan web (tata letak, warna sesuai logo, chat bubble, panel kontrol, tombol ide cepat) dan perbaikan pewarnaan bubble percakapan. |
| `src/prompts.py` | Penyempurnaan *system prompt*: perluasan cakupan dari tanaman cabai ke berbagai tanaman, penyusunan alur konsultasi, aturan keamanan, dan contoh percakapan (*few-shot*). |
| `data/knowledge_base.json` | Penyusunan draf perluasan data dari 3 kasus (cabai) menjadi 32 kasus (cabai, tomat, padi, jagung, dan panduan umum) beserta penambahan field baru. Isi data disusun dari pengetahuan agronomi umum dan sebaiknya tetap diverifikasi kepada penyuluh pertanian. |
| `src/knowledge_base.py` dan `src/conversation.py` | Penambahan mekanisme pemilihan kasus yang relevan dan pembatasan riwayat untuk mengatasi galat batas token (*rate limit*) pada Groq API. |
| `src/chatbot.py` | Perbaikan agar riwayat yang disimpan tetap lengkap dan pesan galat API tidak tersimpan sebagai jawaban asisten. |
| Debugging dan dokumentasi | Bantuan menelusuri pesan galat selama pengembangan (kesalahan pembacaan JSON, ketidaksesuaian format data, dan batas token) serta penyusunan kalimat pada README ini. |

**Bagian yang dikerjakan mandiri:**

| Bagian | Keterangan |
|---|---|
| Tema dan konsep | Penentuan tema asisten konsultasi pertanian dan konsep konsultasi bertahap. |
| Kerangka program | Perancangan struktur proyek dan pembuatan versi awal modul (`config.py`, `llm_client.py`, `commands.py`, `chatbot.py`, `conversation.py`, `main.py`). |
| Versi awal prompt dan data | Penyusunan *system prompt* awal dan data awal pada `knowledge_base.json`. |
| Integrasi API | Pembuatan akun dan API Key Groq, pengaturan file `.env`, serta penghubungan program ke Groq API. |
| Pengujian | Menjalankan program, mencoba berbagai skenario percakapan, dan memeriksa hasilnya di terminal maupun web. |
| Dokumentasi | Pengambilan cuplikan layar, penyusunan repositori GitHub, dan penulisan kerangka awal README. |

Seluruh keluaran dari AI dijalankan dan diuji langsung oleh penulis sebelum digunakan pada proyek ini.