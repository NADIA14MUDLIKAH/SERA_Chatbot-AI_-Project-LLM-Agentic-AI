import sys
import base64
import textwrap
from pathlib import Path
import streamlit as st

# Setup Path agar bisa import dari folder src
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.chatbot import SeraChatbot
from src.commands import save_history_to_file  # noqa: F401

# ----------------- PENGATURAN HALAMAN -----------------
st.set_page_config(
    page_title="SERA AI - Asisten Agrikultur",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ----------------- FUNGSI BACA GAMBAR LOGO -----------------
def get_image_base64(*candidates):
    """Coba beberapa lokasi logo, kembalikan base64 dari yang pertama ketemu."""
    for path in candidates:
        try:
            with open(path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except Exception:
            continue
    return ""


PROJECT_ROOT = Path(__file__).resolve().parent.parent
logo_base64 = get_image_base64(PROJECT_ROOT / "logo.jpg", "logo.jpg")


def html(markup: str):
    """Render HTML tanpa risiko dianggap code block oleh markdown."""
    st.markdown(textwrap.dedent(markup).strip(), unsafe_allow_html=True)


# ----------------- KUSTOMISASI CSS (TEMA DARI LOGO SERA) -----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Nunito:wght@400;600;700;800&display=swap');

    :root {
        --sera-red: #D93A1F;
        --sera-red-dark: #B02A14;
        --sera-orange: #F5A524;
        --sera-orange-soft: #FFE3B3;
        --sera-cream: #FFF8EC;
        --sera-line: #F3E2C2;
        --sera-green: #2F8F46;
        --sera-green-dark: #1E6B34;
        --sera-green-soft: #E8F5EA;
        --sera-ink: #3A2A1E;
        --sera-muted: #8A7A6A;
    }

    /* ---------- Dasar halaman ---------- */
    .stApp {
        background: linear-gradient(180deg, #FFFAF0 0%, #FFF2DC 100%);
        color: var(--sera-ink);
        font-family: 'Nunito', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .stApp .stMarkdown, .stApp textarea, .stApp button p {
        font-family: 'Nunito', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    [data-testid="stHeader"] { background: transparent; }
    .stDeployButton, [data-testid="stAppDeployButton"], #MainMenu, footer { display: none !important; }

    .block-container, [data-testid="stMainBlockContainer"] {
        max-width: none !important;
        width: 100% !important;
        padding-top: 0.6rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
        padding-bottom: 7rem;
        box-sizing: border-box;
    }

    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] {
        background: #FFFCF5;
        border-right: 1px solid var(--sera-line);
    }
    [data-testid="stSidebar"] .block-container,
    [data-testid="stSidebarUserContent"] { padding-top: 1.2rem; }

    .side-logo {
        background: #fff;
        border: 1px solid var(--sera-line);
        border-radius: 20px;
        padding: 10px;
        margin-bottom: 6px;
        text-align: center;
        box-shadow: 0 4px 14px rgba(217, 58, 31, 0.06);
    }
    .side-logo img {
        width: 100%;
        max-height: 150px;
        object-fit: contain;
        border-radius: 12px;
        display: block;
    }
    .side-logo-fallback {
        font-family: 'Baloo 2', sans-serif;
        font-size: 30px;
        font-weight: 800;
        color: var(--sera-red);
        line-height: 1.1;
    }

    .side-title {
        font-family: 'Baloo 2', sans-serif;
        font-size: 15px;
        font-weight: 700;
        color: var(--sera-red-dark);
        margin: 20px 0 8px 2px;
    }
    .side-card {
        background: #fff;
        border: 1px solid var(--sera-line);
        border-radius: 14px;
        padding: 12px 14px;
        font-size: 13.5px;
        line-height: 1.5;
        color: var(--sera-muted);
    }
    .side-card b { color: var(--sera-ink); }

    .steps {
        background: var(--sera-green-soft);
        border: 1px solid #CDE8D2;
        border-radius: 14px;
        padding: 12px 14px;
    }
    .step {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 13.5px;
        color: var(--sera-green-dark);
        font-weight: 600;
        padding: 4px 0;
    }
    .step span {
        flex: 0 0 22px;
        height: 22px;
        border-radius: 50%;
        background: var(--sera-green);
        color: #fff;
        font-size: 12px;
        font-weight: 800;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .side-note {
        font-size: 12px;
        line-height: 1.5;
        color: var(--sera-muted);
        margin-top: 14px;
        padding: 0 2px;
    }

    /* ---------- Tombol ---------- */
    .stButton > button {
        background: #fff;
        color: var(--sera-ink);
        border: 1px solid var(--sera-line);
        border-radius: 14px;
        padding: 10px 14px;
        font-weight: 700;
        font-size: 14px;
        justify-content: flex-start;
        text-align: left;
        box-shadow: none;
        transition: border-color 0.15s ease, background 0.15s ease, transform 0.15s ease;
    }
    .stButton > button p { color: inherit; margin: 0; }
    .stButton > button:hover {
        background: #FFF3DC;
        border-color: var(--sera-orange);
        color: var(--sera-red-dark);
        transform: translateY(-1px);
    }
    .stButton > button:focus-visible {
        outline: 3px solid rgba(245, 165, 36, 0.5);
        outline-offset: 2px;
    }
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, #F5701F 0%, #D93A1F 100%);
        color: #fff;
        border: none;
        justify-content: center;
        text-align: center;
        box-shadow: 0 6px 16px rgba(217, 58, 31, 0.28);
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="stBaseButton-primary"]:hover {
        background: linear-gradient(135deg, #E8641A 0%, #B02A14 100%);
        color: #fff;
    }

    /* ---------- Top bar ---------- */
    .topbar {
        width: 100%;
        box-sizing: border-box;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        background: #fff;
        border: 1px solid var(--sera-line);
        border-radius: 18px;
        padding: 10px 16px;
        margin-bottom: 16px;
        box-shadow: 0 4px 14px rgba(217, 58, 31, 0.05);
    }
    .topbar-left { display: flex; align-items: center; gap: 12px; }
    .topbar-icon {
        width: 46px;
        height: 46px;
        border-radius: 12px;
        background: #fff;
        border: 1px solid var(--sera-line);
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        flex: 0 0 46px;
    }

    .topbar-icon img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        padding: 3px;
        box-sizing: border-box;
    }
    .topbar-title {
        font-family: 'Baloo 2', sans-serif;
        font-size: 20px;
        font-weight: 800;
        color: var(--sera-red);
        line-height: 1.1;
    }
    .topbar-sub { font-size: 12px; color: var(--sera-muted); }
    .topbar-right { display: flex; gap: 8px; flex-wrap: wrap; justify-content: flex-end; }
    .pill {
        font-size: 12px;
        font-weight: 700;
        color: var(--sera-ink);
        background: var(--sera-cream);
        border: 1px solid var(--sera-line);
        border-radius: 999px;
        padding: 5px 12px;
        white-space: nowrap;
    }
    .pill.online {
        background: var(--sera-green-soft);
        border-color: #BFE3C6;
        color: var(--sera-green-dark);
    }
    .pill.online::before {
        content: "";
        display: inline-block;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: var(--sera-green);
        margin-right: 6px;
        vertical-align: 1px;
    }

    /* ---------- Hero ---------- */
    .hero {
        width: 100%;
        box-sizing: border-box;
        position: relative;
        overflow: hidden;
        border-radius: 22px;
        padding: 26px 30px;
        margin-bottom: 18px;
        background:
            radial-gradient(circle at 0% 110%, rgba(47, 143, 70, 0.22), transparent 42%),
            linear-gradient(120deg, #FFE7B5 0%, #FFCF80 55%, #FFB86B 100%);
        border: 1px solid #F7CF8C;
    }
    .hero h1 {
        font-family: 'Baloo 2', sans-serif;
        font-size: 32px;
        font-weight: 800;
        line-height: 1.15;
        color: var(--sera-red-dark);
        margin: 0 0 8px 0;
        padding: 0;
        max-width: 70%;
    }
    .hero p {
        font-size: 15px;
        line-height: 1.55;
        color: #5A4130;
        margin: 0 0 14px 0;
        max-width: 68%;
    }
    .chips { display: flex; flex-wrap: wrap; gap: 8px; max-width: 78%; }
    .chip {
        font-size: 12.5px;
        font-weight: 700;
        color: var(--sera-green-dark);
        background: rgba(255, 255, 255, 0.78);
        border: 1px solid rgba(47, 143, 70, 0.25);
        border-radius: 999px;
        padding: 5px 12px;
    }
    .hero-badge {
        position: absolute;
        right: 26px;
        top: 50%;
        transform: translateY(-50%) rotate(-7deg);
        width: 92px;
        height: 92px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.85);
        border: 3px solid #fff;
        box-shadow: 0 8px 22px rgba(176, 42, 20, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 46px;
    }

    /* ---------- Kartu sambutan (kondisi awal) ---------- */
    .welcome { display: flex; align-items: flex-start; gap: 16px; margin: 6px 0 4px 0; }
    .welcome-mascot {
        flex: 0 0 92px;
        height: 92px;
        border-radius: 24px;
        background: #fff;
        border: 1px solid var(--sera-line);
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        box-shadow: 0 6px 16px rgba(245, 165, 36, 0.3);
    }

    .welcome-mascot img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        padding: 5px;
        box-sizing: border-box;
    }
    .welcome-bubble {
        background: #fff;
        border: 1px solid var(--sera-line);
        border-radius: 22px 22px 22px 6px;
        padding: 16px 20px;
        box-shadow: 0 4px 14px rgba(217, 58, 31, 0.05);
    }
    .welcome-tag { font-size: 12px; font-weight: 800; color: var(--sera-green); margin-bottom: 2px; }
    .welcome-bubble h3 {
        font-family: 'Baloo 2', sans-serif;
        font-size: 21px;
        font-weight: 700;
        color: var(--sera-ink);
        margin: 0 0 6px 0;
        padding: 0;
    }
    .welcome-bubble p { font-size: 14.5px; line-height: 1.6; color: #6B5847; margin: 0; }

    /* ---------- Bubble chat ---------- */
    [data-testid="stChatMessage"] {
        background: linear-gradient(135deg, #FFFFFF 0%, #FFF8EA 100%);
        border: 1px solid #F1D39F;
        border-radius: 20px 20px 20px 6px;
        padding: 16px 20px;
        margin-bottom: 16px;
        gap: 0.8rem;
        width: 68%;
        max-width: 760px;
        min-width: 460px;
        box-shadow: 0 6px 18px rgba(217, 58, 31, 0.08);
    }

    /* Chat SERA dibuat lebih lebar dan sedikit masuk ke tengah */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
        margin-left: 0;
        margin-right: auto;
    }
    /* Pesan pengguna: rata kanan, hangat oranye */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        flex-direction: row-reverse;
        margin-left: auto;
        margin-right: 8%;
        width: 48%;
        min-width: 0;
        max-width: 620px;
        background: linear-gradient(135deg, #FFF0C9 0%, #FFDFA8 100%);
        border-color: #F4B95F;
        border-radius: 20px 20px 6px 20px;
    }
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li {
        font-size: 15.5px;
        line-height: 1.65;
        color: var(--sera-ink);
    }
    [data-testid="stChatMessage"] strong { color: var(--sera-red-dark); }

    /* Bubble SERA lebih berwarna */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, #FFFDF7 0%, #FFF4D8 100%);
        border-radius: 14px;
        padding: 10px 14px;
    }

    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) p,
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) li {
        color: #4B382A;
    }

    /* Label kecil di atas bubble */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stChatMessageContent"]::before {
        content: "SERA";
        display: block;
        font-size: 12px;
        font-weight: 800;
        color: var(--sera-green);
        margin-bottom: 2px;
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"]::before {
        content: "Kamu";
        display: block;
        font-size: 12px;
        font-weight: 800;
        color: var(--sera-red);
        margin-bottom: 2px;
    }

    /* Avatar */
    [data-testid="stChatMessageAvatarAssistant"],
    [data-testid="stChatMessageAvatarUser"] {
        width: 38px;
        height: 38px;
        border-radius: 12px;
        font-size: 20px;
    }
    [data-testid="stChatMessageAvatarAssistant"] { background: linear-gradient(135deg, #FFD9A0, #F5A524); }
    [data-testid="stChatMessageAvatarUser"] { background: linear-gradient(135deg, #CDEBD3, #7CC68B); }

    /* ---------- Input chat ---------- */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    [data-testid="stBottomBlockContainer"] { background: transparent; }

    [data-testid="stChatInput"] {
        background: #fff;
        border: 2px solid var(--sera-orange);
        border-radius: 999px;
        box-shadow: 0 8px 22px rgba(245, 165, 36, 0.2);
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: var(--sera-red);
        box-shadow: 0 8px 22px rgba(217, 58, 31, 0.2);
    }
    [data-testid="stChatInput"] textarea {
        background: transparent;
        color: var(--sera-ink);
        font-size: 15px;
    }
    [data-testid="stChatInput"] textarea::placeholder { color: #B5A48F; }
    [data-testid="stChatInput"] button {
        background: linear-gradient(135deg, #F5701F 0%, #D93A1F 100%);
        color: #fff;
        border-radius: 50%;
    }

    /* ---------- Responsif ---------- */
    @media (max-width: 720px) {
        .hero h1, .hero p, .chips { max-width: 100%; }
        .hero-badge { display: none; }
        .topbar-right .pill:not(.online) { display: none; }
        [data-testid="stChatMessage"] {
            width: 92%;
            max-width: none;
            min-width: 0;
        }

        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
            width: 82%;
            margin-right: 0;
        }
    }
</style>
""", unsafe_allow_html=True)

# ----------------- INISIALISASI SESSION STATE -----------------
if "chatbot" not in st.session_state:
    st.session_state.chatbot = SeraChatbot()
if "messages_ui" not in st.session_state:
    st.session_state.messages_ui = []

AVATARS = {"user": "🧑‍🌾", "assistant": "🌶️"}

# Contoh pertanyaan cepat: (label tombol, teks yang dikirim)
QUICK_IDEAS = [
    ("🍂  Daun menguning", "Daun tanamanku menguning, kenapa ya?"),
    ("🌀  Daun keriting", "Daun tanamanku keriting dan menggulung, kenapa ya?"),
    ("🥀  Tanaman layu", "Tanamanku tiba-tiba layu padahal sudah disiram."),
    ("🐛  Ada hama", "Ada hama atau serangga di tanamanku, tolong bantu identifikasi."),
]


def send_quick_idea(text: str):
    st.session_state.pending_input = text


# ----------------- PROSES INPUT (sebelum render, supaya tampilan langsung sinkron) -----------------
pending = st.session_state.pop("pending_input", None)
user_input = st.chat_input("Ketik gejala pada tanaman Anda di sini...") or pending

if user_input:
    st.session_state.messages_ui.append({"role": "user", "content": user_input})

# ----------------- SIDEBAR -----------------
with st.sidebar:
    if logo_base64:
        html(f"""
        <div class="side-logo">
            <img src="data:image/jpeg;base64,{logo_base64}" alt="Logo SERA">
        </div>
        """)
    else:
        html("""
        <div class="side-logo"><div class="side-logo-fallback">SERA</div></div>
        """)

    html('<div class="side-title">🌾 Sesi ini</div>')
    n_user = sum(1 for m in st.session_state.messages_ui if m["role"] == "user")
    if n_user == 0:
        html('<div class="side-card">Belum ada cerita.<br>Ceritakan kondisi tanamanmu, ya!</div>')
    else:
        html(f'<div class="side-card"><b>{n_user}</b> pesan sudah kamu kirim di sesi ini.</div>')

    html('<div class="side-title">⚡ Ide cepat</div>')
    for i, (label, text) in enumerate(QUICK_IDEAS):
        st.button(label, key=f"quick_{i}", use_container_width=True,
                  on_click=send_quick_idea, args=(text,))

    html("""
    <div class="side-title">🌱 Cara kerja SERA</div>
    <div class="steps">
        <div class="step"><span>1</span>Ceritakan gejala tanamanmu</div>
        <div class="step"><span>2</span>Jawab pertanyaan dari SERA</div>
        <div class="step"><span>3</span>Terima rekomendasi penanganan</div>
    </div>
    """)

    html('<div style="height: 18px"></div>')

    if st.button("💾  Simpan riwayat", key="save", use_container_width=True):
        if st.session_state.messages_ui:
            filepath = st.session_state.chatbot.save()
            st.success(f"Tersimpan di: {filepath}")
        else:
            st.warning("Belum ada percakapan.")

    if st.button("✨  Percakapan baru", key="reset", type="primary", use_container_width=True):
        st.session_state.chatbot.reset()
        st.session_state.messages_ui = []
        st.rerun()

    html("""
    <div class="side-note">
        SERA memberi saran awal. Untuk kasus berat, tetap konsultasikan dengan penyuluh pertanian setempat.
    </div>
    """)

# ----------------- HEADER UTAMA -----------------
html(f"""
<div class="topbar">
    <div class="topbar-left">
        <div class="topbar-icon">
            <img src="data:image/jpeg;base64,{logo_base64}" alt="Logo SERA">
        </div>
        <div>
            <div class="topbar-title">SERA</div>
            <div class="topbar-sub">Sistem Edukasi &amp; Rekomendasi Agrikultur</div>
        </div>
    </div>
    <div class="topbar-right">
        <span class="pill">🩺 Diagnosis bertahap</span>
        <span class="pill online">AI aktif</span>
    </div>
</div>
""")

html("""
<div class="hero">
    <h1>Tanamanmu lagi kenapa? 🔍</h1>
    <p>Ceritakan gejala yang kamu lihat. SERA bantu cari penyebabnya selangkah demi selangkah, lalu kasih saran penanganan yang pas.</p>
    <div class="chips">
        <span class="chip">🔎 Identifikasi gejala</span>
        <span class="chip">🪜 Tanya bertahap</span>
        <span class="chip">💊 Saran penanganan</span>
        <span class="chip">🌿 Edukasi budidaya</span>
    </div>
    <div class="hero-badge">🌱</div>
</div>
""")

# ----------------- CHAT INTERFACE -----------------
if not st.session_state.messages_ui:
    html(f"""
    <div class="welcome">
        <div class="welcome-mascot">
            <img src="data:image/jpeg;base64,{logo_base64}" alt="Logo SERA">
        </div>
        <div class="welcome-bubble">
            <div class="welcome-tag">SERA, teman tanimu</div>
            <h3>Halo! Aku SERA, siap bantu tanamanmu 🌱</h3>
            <p>Mulai dengan cerita singkat: tanaman apa yang kamu tanam dan apa yang terlihat aneh. Nanti aku tanya-tanya sedikit supaya diagnosisnya tepat.</p>
        </div>
    </div>
    """)

for msg in st.session_state.messages_ui:
    with st.chat_message(msg["role"], avatar=AVATARS.get(msg["role"])):
        st.markdown(msg["content"])

if user_input:
    with st.chat_message("assistant", avatar=AVATARS["assistant"]):
        response_placeholder = st.empty()
        full_response = ""

        for chunk in st.session_state.chatbot.chat_stream(user_input):
            full_response += chunk
            response_placeholder.markdown(full_response + "▌")

        response_placeholder.markdown(full_response)

    st.session_state.messages_ui.append({"role": "assistant", "content": full_response})