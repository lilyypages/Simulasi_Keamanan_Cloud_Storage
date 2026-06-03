import os
import sys
import time
import json
import shutil
from datetime import datetime
from PIL import Image

import streamlit as st

# Ensure project root is in the system path for imports
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from crypto import aes_util, rsa_util, hash_util
from stego import lsb
from blockchain import blockchain
from utils.workflow import secure_file, recover_file

# Set up page configurations
st.set_page_config(
    page_title="Cloud Stego-Guard | Multilayer Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create folders if not exist
os.makedirs("storage/uploads", exist_ok=True)
os.makedirs("storage/encrypted", exist_ok=True)
os.makedirs("storage/stego_images", exist_ok=True)
os.makedirs("storage/decrypted", exist_ok=True)
os.makedirs("storage/temp", exist_ok=True)
os.makedirs("keys", exist_ok=True)

# Custom premium styling (Dark Mode & Glassmorphism)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Outfit', sans-serif;
    background-color: #DDEEEA !important;
    color: #212529 !important;
}

[data-testid="stSidebar"] {
    background-color: #FFC400 !important;
    border-right: none;
    border-radius: 0 35px 35px 0;
    box-shadow: 5px 0 20px rgba(0,0,0,0.08);
    min-width: 260px !important;
    max-width: 260px !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p, 
[data-testid="stSidebar"] span, [data-testid="stSidebar"] h1 {
    color: #212529 !important;
}

code, pre {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
}

/* Custom card container (Light Pastel Version) */
.glass-card {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
    color: #212529;
}

.glass-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.08);
}

/* Gradient header title (Darker for Light Mode) */
.gradient-title {
    background: linear-gradient(135deg, #4f46e5 0%, #059669 50%, #0284c7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 0px;
    letter-spacing: -0.5px;
}

.glow-text {
    text-shadow: none;
}

.subtitle {
    color: #475569;
    font-size: 1.1rem;
    margin-bottom: 30px;
}

/* Status Badges */
.status-badge {
    padding: 5px 12px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.85rem;
    display: inline-block;
}

.badge-success {
    background-color: rgba(16, 185, 129, 0.15);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.badge-warning {
    background-color: rgba(245, 158, 11, 0.15);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.3);
}

.badge-danger {
    background-color: rgba(239, 68, 68, 0.15);
    color: #ef4444;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

.badge-info {
    background-color: rgba(99, 102, 241, 0.15);
    color: #818cf8;
    border: 1px solid rgba(99, 102, 241, 0.3);
}

/* Step cards for recovery logging */
.step-card {
    border-left: 4px solid #4f46e5;
    background: #FFFFFF;
    padding: 15px 20px;
    border-radius: 0 12px 12px 0;
    margin-bottom: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    transition: all 0.3s ease;
}

.step-success {
    border-left-color: #10b981 !important;
    background: rgba(16, 185, 129, 0.05);
}

.step-failed {
    border-left-color: #ef4444 !important;
    background: rgba(239, 68, 68, 0.05);
}

.step-title {
    font-weight: 700;
    font-size: 1.05rem;
    margin-bottom: 4px;
}

.step-desc {
    font-size: 0.9rem;
    color: #475569;
}

/* Sidebar styling overrides */
.css-17eq0hr, [data-testid="stSidebarNav"] {
    background-color: transparent !important;
}

/* Hilangkan bar putih kosong di bagian paling atas (Header) */
header[data-testid="stHeader"] {
    background-color: transparent !important;
    box-shadow: none !important;
}

/* Sembunyikan tombol Deploy dan Menu tiga titik (Toolbar) */
.stDeployButton {display: none !important;}
[data-testid="stToolbar"] {display: none !important;}

/* Radio button text sidebar (Dibuat lebih lega dan mulus) */
div.stRadio > div[role="radiogroup"] > label > div:first-child {
    display: none !important;
}
div.stRadio > div[role="radiogroup"] > label {
    margin-bottom: 12px;
    padding: 15px 25px;
    border-radius: 12px;
    transition: all 0.3s ease;
    cursor: pointer;
    width: 100%;
    display: block;
}
div.stRadio > div[role="radiogroup"] > label:hover {
    background-color: rgba(255, 255, 255, 0.4);
    transform: translateX(4px);
}
/* Style saat menu aktif / diklik */
div.stRadio > div[role="radiogroup"] > label:has(input:checked) {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    font-weight: 800 !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    transform: translateX(4px);
}

/* Custom Divider line */
.divider {
    height: 1px;
    background: rgba(0, 0, 0, 0.08);
    margin: 25px 0;
}
</style>
""", unsafe_allow_html=True)

# Helper function to clear temp files
def clear_temp():
    if os.path.exists("storage/temp"):
        shutil.rmtree("storage/temp")
    os.makedirs("storage/temp", exist_ok=True)

# Navigation setup
st.sidebar.markdown(
    '<div style="text-align: center; padding: 10px 0;">'
    '<h1 style="color: #111827; font-size: 1.4rem; font-weight: 900; margin-bottom: 0;">🛡️ STEGO-GUARD</h1>'
    '<p style="color: #475569; font-size: 0.8rem; margin-top: 4px; font-weight: 600;">Multilayer Simulator</p>'
    '</div>',
    unsafe_allow_html=True
)

st.sidebar.markdown('<div class="divider"></div>', unsafe_allow_html=True)

menu = st.sidebar.radio(
    "NAVIGATION MENU",
    ["📊 Dashboard Overview", "🔒 Secure File Page", "🔑 Recover File Page", "🔗 Blockchain Explorer"],
    index=0,
    label_visibility="collapsed"
)

st.sidebar.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Sidebar system status widget
chain_valid = blockchain.verify_blockchain()
chain_len = len(blockchain.load_blockchain())

st.sidebar.markdown('<p style="font-weight:800; color:#111827; font-size:0.85rem; margin-bottom:8px;">SYSTEM STATUS</p>', unsafe_allow_html=True)
if chain_valid:
    st.sidebar.markdown('<span class="status-badge badge-success" style="background-color: #FFFFFF; border-color: #10b981; font-weight: 800;">● Blockchain Secured</span>', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<span class="status-badge badge-danger" style="background-color: #FFFFFF; border-color: #ef4444; font-weight: 800;">● Blockchain Corrupted</span>', unsafe_allow_html=True)

st.sidebar.markdown(f'<p style="font-size:0.85rem; color:#475569; font-weight:600; margin-top:8px;">Ledger Height: <b style="color:#111827;">{chain_len} Blocks</b></p>', unsafe_allow_html=True)

# ----------------- PAGE 1: DASHBOARD OVERVIEW -----------------
if menu == "📊 Dashboard Overview":
    st.markdown('<h1 class="gradient-title">📊 Security Overview</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Sistem keamanan multilayer berbasis Kriptografi AES-256, RSA-2048, Hashing SHA-256, Steganografi LSB, dan Blockchain</p>', unsafe_allow_html=True)

    # Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            '<div class="glass-card">'
            '<p style="color:#64748b; font-weight:600; font-size:0.85rem; text-transform:uppercase; margin-bottom:4px;">Kriptografi Simetris</p>'
            '<h3 style="color:#22d3ee; margin:0; font-size:1.8rem;">AES-256-CBC</h3>'
            '<p style="color:#475569; font-size:0.75rem; margin-top:4px;">Enkripsi berkas data utama</p>'
            '</div>', 
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            '<div class="glass-card">'
            '<p style="color:#64748b; font-weight:600; font-size:0.85rem; text-transform:uppercase; margin-bottom:4px;">Kriptografi Asimetris</p>'
            '<h3 style="color:#818cf8; margin:0; font-size:1.8rem;">RSA-2048</h3>'
            '<p style="color:#475569; font-size:0.75rem; margin-top:4px;">Proteksi kunci AES via pemaketan kunci</p>'
            '</div>', 
            unsafe_allow_html=True
        )
    with col3:
        # Count encrypted files
        enc_count = len([f for f in os.listdir("storage/encrypted") if f.endswith(".enc")])
        st.markdown(
            f'<div class="glass-card">'
            f'<p style="color:#64748b; font-weight:600; font-size:0.85rem; text-transform:uppercase; margin-bottom:4px;">Berkas Terenkripsi</p>'
            f'<h3 style="color:#34d399; margin:0; font-size:1.8rem;">{enc_count} Files</h3>'
            f'<p style="color:#475569; font-size:0.75rem; margin-top:4px;">Disimpan di storage/encrypted</p>'
            f'</div>', 
            unsafe_allow_html=True
        )
    with col4:
        st.markdown(
            f'<div class="glass-card">'
            f'<p style="color:#64748b; font-weight:600; font-size:0.85rem; text-transform:uppercase; margin-bottom:4px;">Steganografi LSB</p>'
            f'<h3 style="color:#f472b6; margin:0; font-size:1.8rem;">PNG Carrier</h3>'
            f'<p style="color:#475569; font-size:0.75rem; margin-top:4px;">Metadata tersembunyi pada bit citra</p>'
            f'</div>', 
            unsafe_allow_html=True
        )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    left_col, right_col = st.columns([3, 2])

    with left_col:
        st.markdown('<h3 style="color:#111827; font-weight:700;">🔄 Alur Keamanan Multilayer</h3>', unsafe_allow_html=True)
        st.markdown(
            '<div class="glass-card" style="padding: 25px;">'
            '<p style="font-size: 0.95rem; line-height: 1.6; margin-bottom: 20px;">'
            'Aplikasi ini menyimulasikan perlindungan data sensitif sebelum diunggah ke cloud storage menggunakan 5 lapis pengamanan terpadu:'
            '</p>'
            '<ol style="padding-left: 20px; line-height: 2.0; font-size:0.95rem;">'
            '<li><b>Lapis 1 (AES-256):</b> Berkas data sensitif dienkripsi menjadi berkas format `.enc` menggunakan kunci simetris 256-bit secara chunked (efisien untuk file besar).</li>'
            '<li><b>Lapis 2 (RSA-2048):</b> Kunci AES-256 yang dinamis dienkripsi secara asimetris menggunakan kunci publik RSA milik pengguna, memecahkan masalah distribusi kunci.</li>'
            '<li><b>Lapis 3 (SHA-256):</b> Nilai hash (sidik jari digital) dari berkas terenkripsi `.enc` dihitung secara presisi untuk memvalidasi integritas di kemudian hari.</li>'
            '<li><b>Lapis 4 (Blockchain):</b> Nilai hash disimpan secara permanen di dalam buku kas blockchain terdesentralisasi (berbasis rantai JSON) untuk jaminan anti-modifikasi.</li>'
            '<li><b>Lapis 5 (Steganografi LSB):</b> Kunci AES terenkripsi beserta nama berkas asli dan hash diinjeksikan secara kasat mata ke dalam saluran bit piksel gambar cover (Stego Image).</li>'
            '</ol>'
            '</div>',
            unsafe_allow_html=True
        )

    with right_col:
        st.markdown('<h3 style="color:#111827; font-weight:700;">🔑 Manajemen Kunci RSA</h3>', unsafe_allow_html=True)
        
        priv_exists = os.path.exists("keys/private.pem")
        pub_exists = os.path.exists("keys/public.pem")

        if priv_exists and pub_exists:
            st.markdown(
                '<div style="margin-bottom:15px;">'
                '<span class="status-badge badge-success">● RSA Key Pair Aktif</span>'
                '</div>',
                unsafe_allow_html=True
            )
            with st.expander("Tampilkan Informasi Kunci"):
                with open("keys/public.pem", "r") as f:
                    st.code(f.read(), language="text")
        else:
            st.markdown(
                '<div style="margin-bottom:15px;">'
                '<span class="status-badge badge-warning">▲ Kunci RSA Belum Dibuat</span>'
                '</div>',
                unsafe_allow_html=True
            )

        with st.form("rsa_gen_form"):
            st.markdown('<p style="font-weight:600; margin-bottom:5px;">Buat Kunci RSA Baru</p>', unsafe_allow_html=True)
            passphrase = st.text_input("Masukkan Passphrase Kunci Privat", type="password", help="Kunci privat akan dienkripsi dengan passphrase ini")
            submit_gen = st.form_submit_button("Generate RSA Key Pair")

            if submit_gen:
                if not passphrase:
                    st.error("Gagal: Silakan masukkan passphrase terlebih dahulu!")
                else:
                    with st.spinner("Membuat kunci RSA 2048-bit..."):
                        rsa_util.generate_rsa_keys(passphrase=passphrase)
                    st.success("Sukses! Kunci RSA berhasil digenerate di folder `keys/`")
                    st.rerun()

# ----------------- PAGE 2: SECURE FILE PAGE -----------------
elif menu == "🔒 Secure File Page":
    st.markdown('<h1 class="gradient-title">🔒 Secure & Encrypt File</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Lakukan pengamanan data berlapis: enkripsi data, pasang blockchain hash, dan sisipkan metadata ke gambar stego</p>', unsafe_allow_html=True)

    # Check RSA keys
    if not os.path.exists("keys/public.pem"):
        st.warning("⚠️ Kunci publik RSA tidak terdeteksi. Silakan buat Key Pair terlebih dahulu di Dashboard!")
    else:
        left, right = st.columns([1, 1])

        with left:
            st.markdown('<h4 style="color:#4f46e5;">Upload Berkas & Cover</h4>', unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader("Upload File Sensitif (Apapun)", type=None)
            
            use_default_cover = st.checkbox("Gunakan gambar cover default (assets/cover.png)", value=True)
            
            uploaded_cover = None
            if not use_default_cover:
                uploaded_cover = st.file_uploader("Upload Gambar Cover Kustom (PNG)", type=["png"])

        with right:
            st.markdown('<h4 style="color:#4f46e5;">Konfigurasi Keamanan</h4>', unsafe_allow_html=True)
            st.markdown(
                '<div class="glass-card" style="padding: 20px;">'
                '<ul style="padding-left: 20px; font-size:0.9rem;">'
                '<li><b>Enkripsi:</b> AES-256-CBC otomatis.</li>'
                '<li><b>Distribusi Kunci:</b> Kunci AES dienkripsi dengan <code>keys/public.pem</code>.</li>'
                '<li><b>Integritas:</b> Hash berkas diunggah ke Blockchain.</li>'
                '</ul>'
                '</div>',
                unsafe_allow_html=True
            )

            # Clear old secure result if upload changes
            uploaded_name = uploaded_file.name if uploaded_file else ""
            if "last_uploaded_file" not in st.session_state or st.session_state["last_uploaded_file"] != uploaded_name:
                st.session_state["last_uploaded_file"] = uploaded_name
                if "secure_result" in st.session_state:
                    del st.session_state["secure_result"]

            # Process Button
            if uploaded_file:
                if st.button("🚀 Mulai Proses Pengamanan Berkas"):
                    clear_temp()
                    
                    # Save secret file to temp
                    secret_temp_path = f"storage/temp/{uploaded_file.name}"
                    with open(secret_temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    # Determine cover image
                    cover_path = "assets/cover.png"
                    if not use_default_cover:
                        if uploaded_cover:
                            cover_path = f"storage/temp/{uploaded_cover.name}"
                            with open(cover_path, "wb") as f:
                                f.write(uploaded_cover.getbuffer())
                        else:
                            st.error("Silakan unggah gambar cover kustom atau pilih opsi cover default!")
                            st.stop()

                    # Run workflow
                    progress_text = "Menjalankan pipeline keamanan..."
                    my_bar = st.progress(0, text=progress_text)
                    
                    try:
                        time.sleep(0.3)
                        my_bar.progress(20, text="[Lapis 1] Mengenkripsi berkas dengan AES-256...")
                        
                        time.sleep(0.3)
                        my_bar.progress(40, text="[Lapis 2] Melindungi kunci AES dengan Kunci Publik RSA...")
                        
                        time.sleep(0.3)
                        my_bar.progress(60, text="[Lapis 3] Menghitung SHA-256 hash berkas terenkripsi...")
                        
                        time.sleep(0.3)
                        my_bar.progress(80, text="[Lapis 4] Mendaftarkan hash ke Blockchain Ledger...")
                        
                        # Call backend secure function
                        result = secure_file(secret_temp_path, cover_path)
                        
                        time.sleep(0.3)
                        my_bar.progress(100, text="[Lapis 5] Menyisipkan metadata (Steganografi LSB)... Selesai!")
                        
                        # Store result in session state
                        st.session_state["secure_result"] = result
                        
                    except Exception as e:
                        st.error(f"Terjadi kesalahan saat pengamanan berkas: {str(e)}")

                # Render download buttons from session state if available
                if "secure_result" in st.session_state:
                    result = st.session_state["secure_result"]
                    st.success("🎉 Pengamanan data berlapis berhasil diselesaikan!")
                    
                    # Display Results and Download Buttons
                    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                    st.markdown('### 📥 Unduh Hasil Pengamanan Berkas', unsafe_allow_html=True)
                    
                    d_col1, d_col2 = st.columns(2)
                    
                    with d_col1:
                        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                        st.markdown('##### 1. Berkas Terenkripsi (`.enc`)')
                        st.markdown(f'<code style="font-size:0.8rem;">{os.path.basename(result["encrypted_file"])}</code>', unsafe_allow_html=True)
                        with open(result["encrypted_file"], "rb") as f:
                            st.download_button(
                                label="Download Encrypted File (.enc)",
                                data=f.read(),
                                file_name=os.path.basename(result["encrypted_file"]),
                                mime="application/octet-stream",
                                key="btn_download_enc"
                            )
                        st.markdown('</div>', unsafe_allow_html=True)

                    with d_col2:
                        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                        st.markdown('##### 2. Gambar Steganografi (`_stego.png`)')
                        st.markdown(f'<code style="font-size:0.8rem;">{os.path.basename(result["stego_image"])}</code>', unsafe_allow_html=True)
                        with open(result["stego_image"], "rb") as f:
                            st.download_button(
                                label="Download Stego Image (.png)",
                                data=f.read(),
                                file_name=os.path.basename(result["stego_image"]),
                                mime="image/png",
                                key="btn_download_stego"
                            )
                        st.markdown('</div>', unsafe_allow_html=True)

                    # Show details info
                    st.info(f"**SHA-256 Hash Terdaftar:** `{result['hash']}`")
            else:
                st.info("💡 Silakan unggah berkas data sensitif terlebih dahulu di kolom kiri.")


# ----------------- PAGE 3: RECOVER FILE PAGE -----------------
elif menu == "🔑 Recover File Page":
    st.markdown('<h1 class="gradient-title">🔑 Decrypt & Recover File</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Gunakan saluran audit interaktif untuk mengekstrak stego, memvalidasi integritas blockchain, mencocokkan SHA-256, dan memulihkan file asli</p>', unsafe_allow_html=True)

    col_inputs, col_audit = st.columns([2, 3])

    with col_inputs:
        st.markdown('<h3 style="color:#4f46e5; font-size:1.3rem; font-weight:700;">📂 Input Bahan Pemulihan</h3>', unsafe_allow_html=True)
        
        stego_upload = st.file_uploader("1. Unggah Gambar Stego (PNG)", type=["png"])
        enc_upload = st.file_uploader("2. Unggah Berkas Terenkripsi (.enc)", type=["enc"])
        
        st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
        
        # Private key option
        key_option = st.selectbox(
            "3. Opsi Kunci Privat RSA",
            ["Gunakan Kunci Lokal (keys/private.pem)", "Unggah Kunci Privat Kustom (.pem)"]
        )
        
        custom_key_upload = None
        if key_option == "Unggah Kunci Privat Kustom (.pem)":
            custom_key_upload = st.file_uploader("Unggah berkas Kunci Privat RSA (.pem)", type=["pem"])
            
        passphrase_input = st.text_input("4. Passphrase Kunci Privat", type="password", help="Passphrase yang digunakan saat generate key pair")

        st.markdown('<div style="height:15px;"></div>', unsafe_allow_html=True)
        
        # Trigger button
        recover_btn = st.button("🚀 Start Deep Recovery Audit", use_container_width=True)

    with col_audit:
        st.markdown('<h3 style="color:#4f46e5; font-size:1.3rem; font-weight:700;">🔍 Diagnostic Security Audit Logs</h3>', unsafe_allow_html=True)
        
        # Clear old recover results if uploads change
        stego_name = stego_upload.name if stego_upload else ""
        enc_name = enc_upload.name if enc_upload else ""
        upload_key = f"{stego_name}_{enc_name}"
        
        if "last_recover_uploads" not in st.session_state or st.session_state["last_recover_uploads"] != upload_key:
            st.session_state["last_recover_uploads"] = upload_key
            if "recover_result" in st.session_state:
                del st.session_state["recover_result"]
            if "recover_logs" in st.session_state:
                del st.session_state["recover_logs"]

        if recover_btn:
            if not stego_upload:
                st.error("Kesalahan: Gambar stego belum diunggah!")
            elif not enc_upload:
                st.error("Kesalahan: Berkas terenkripsi (.enc) belum diunggah!")
            elif key_option == "Unggah Kunci Privat Kustom (.pem)" and not custom_key_upload:
                st.error("Kesalahan: Anda memilih kunci privat kustom tetapi berkas belum diunggah!")
            else:
                clear_temp()

                # Save uploaded assets to temp files
                temp_stego = f"storage/temp/stego_{stego_upload.name}"
                with open(temp_stego, "wb") as f:
                    f.write(stego_upload.getbuffer())

                temp_enc = f"storage/temp/enc_{enc_upload.name}"
                with open(temp_enc, "wb") as f:
                    f.write(enc_upload.getbuffer())

                # Determine private key file
                private_key_path = "keys/private.pem"
                if key_option == "Unggah Kunci Privat Kustom (.pem)":
                    private_key_path = "storage/temp/custom_private.pem"
                    with open(private_key_path, "wb") as f:
                        f.write(custom_key_upload.getbuffer())
                
                # Check private key existence
                if not os.path.exists(private_key_path):
                    st.error("Kesalahan: Kunci privat RSA tidak ditemukan. Silakan cek folder keys/ atau unggah file kunci Anda.")
                    st.stop()

                # Step placeholders
                step1 = st.empty()
                step2 = st.empty()
                step3 = st.empty()
                step4 = st.empty()
                step5 = st.empty()

                metadata = None
                aes_key = None
                logs = {}
                
                # ----------------- STEP 1: METADATA EXTRACTION -----------------
                step1.markdown(
                    '<div class="step-card">'
                    '<div class="step-title">🔍 Step 1: Extracting Metadata from Stego Image...</div>'
                    '<div class="step-desc">Membaca piksel bit terendah (LSB) pada gambar stego untuk mengekstrak JSON metadata keamanan.</div>'
                    '</div>', 
                    unsafe_allow_html=True
                )
                time.sleep(1.0)
                
                try:
                    metadata = lsb.extract_metadata(temp_stego)
                    if metadata is None:
                        raise Exception("Pengekstrakan gagal. Gambar tidak memiliki stego yang valid atau berkas rusak.")
                    
                    trunc_key = metadata["encrypted_key"][:30] + "..." if len(metadata["encrypted_key"]) > 30 else metadata["encrypted_key"]
                    
                    log_html = f'<div class="step-card step-success"><div class="step-title" style="color:#10b981;">✔️ Step 1: Metadata Extracted Successfully</div><div class="step-desc">• Nama Berkas Asli: <b>{metadata["filename"]}</b><br>• Kunci AES Terproteksi RSA: <code style="font-size:0.75rem;">{trunc_key}</code><br>• SHA-256 Asli: <code style="font-size:0.75rem;">{metadata["hash"]}</code></div></div>'
                    step1.markdown(log_html, unsafe_allow_html=True)
                    logs["step1"] = log_html
                except Exception as e:
                    log_html = f'<div class="step-card step-failed"><div class="step-title" style="color:#ef4444;">❌ Step 1: Metadata Extraction Failed</div><div class="step-desc">{str(e)}</div></div>'
                    step1.markdown(log_html, unsafe_allow_html=True)
                    logs["step1"] = log_html
                    st.session_state["recover_logs"] = logs
                    st.stop()

                # ----------------- STEP 2: BLOCKCHAIN INTEGRITY CHECK -----------------
                step2.markdown(
                    '<div class="step-card">'
                    '<div class="step-title">🔗 Step 2: Running Blockchain Cryptographic Audit...</div>'
                    '<div class="step-desc">Memverifikasi seluruh keterkaitan hash blok pada blockchain ledger untuk mendeteksi manipulasi eksternal.</div>'
                    '</div>', 
                    unsafe_allow_html=True
                )
                time.sleep(1.0)

                try:
                    is_blockchain_valid = blockchain.verify_blockchain()
                    if not is_blockchain_valid:
                        raise Exception("Rantai hash Blockchain rusak! Terjadi tampering pada data ledger utama.")
                    
                    chain = blockchain.load_blockchain()
                    hash_exists = False
                    block_idx = -1
                    for block in chain:
                        if block["file_hash"] == metadata["hash"]:
                            hash_exists = True
                            block_idx = block["index"]
                            break
                    
                    if not hash_exists:
                        raise Exception(f"Hash berkas ({metadata['hash'][:12]}...) TIDAK terdaftar di blockchain ledger mana pun.")
                    
                    log_html = f'<div class="step-card step-success"><div class="step-title" style="color:#10b981;">✔️ Step 2: Blockchain Verification Passed</div><div class="step-desc">• Keutuhan Ledger: <b>Valid & Aman</b><br>• Posisi Blok Terdaftar: <b>Block #{block_idx}</b></div></div>'
                    step2.markdown(log_html, unsafe_allow_html=True)
                    logs["step2"] = log_html
                except Exception as e:
                    log_html = f'<div class="step-card step-failed"><div class="step-title" style="color:#ef4444;">❌ Step 2: Blockchain Verification Failed</div><div class="step-desc">{str(e)}</div></div>'
                    step2.markdown(log_html, unsafe_allow_html=True)
                    logs["step2"] = log_html
                    st.session_state["recover_logs"] = logs
                    st.stop()

                # ----------------- STEP 3: FILE INTEGRITY CHECK (SHA-256) -----------------
                step3.markdown(
                    '<div class="step-card">'
                    '<div class="step-title">🛡️ Step 3: Checking File SHA-256 Integrity...</div>'
                    '<div class="step-desc">Menghitung ulang hash SHA-256 dari berkas terenkripsi (.enc) yang diunggah dan mencocokkannya dengan nilai asli.</div>'
                    '</div>', 
                    unsafe_allow_html=True
                )
                time.sleep(1.0)

                try:
                    uploaded_file_hash = hash_util.generate_file_hash(temp_enc)
                    if uploaded_file_hash != metadata["hash"]:
                        raise Exception(
                            f"Kecocokan Hash Gagal!<br>"
                            f"• Hash Berkas Diunggah: <code>{uploaded_file_hash[:16]}...</code><br>"
                            f"• Hash Seharusnya: <code>{metadata['hash'][:16]}...</code><br>"
                            f"Berkas telah dimodifikasi atau dirusak saat transit!"
                        )
                    
                    log_html = f'<div class="step-card step-success"><div class="step-title" style="color:#10b981;">✔️ Step 3: SHA-256 Hash Verification Match</div><div class="step-desc">• Hash Berkas Diunggah: <code style="font-size:0.75rem;">{uploaded_file_hash}</code> (100% Cocok)</div></div>'
                    step3.markdown(log_html, unsafe_allow_html=True)
                    logs["step3"] = log_html
                except Exception as e:
                    log_html = f'<div class="step-card step-failed"><div class="step-title" style="color:#ef4444;">❌ Step 3: File Integrity Check Failed</div><div class="step-desc">{str(e)}</div></div>'
                    step3.markdown(log_html, unsafe_allow_html=True)
                    logs["step3"] = log_html
                    st.session_state["recover_logs"] = logs
                    st.stop()

                # ----------------- STEP 4: RSA KEY DECRYPTION -----------------
                step4.markdown(
                    '<div class="step-card">'
                    '<div class="step-title">🔑 Step 4: Decrypting AES Key using RSA Private Key...</div>'
                    '<div class="step-desc">Membaca kunci privat RSA dan menggunakan passphrase untuk mendekripsi kunci AES simetris.</div>'
                    '</div>', 
                    unsafe_allow_html=True
                )
                time.sleep(1.0)

                try:
                    aes_key = rsa_util.decrypt_aes_key(
                        metadata["encrypted_key"],
                        private_key_path=private_key_path,
                        passphrase=passphrase_input if passphrase_input else None
                    )
                    trunc_aes_key = aes_key.hex()[:16] + "..."
                    
                    log_html = f'<div class="step-card step-success"><div class="step-title" style="color:#10b981;">✔️ Step 4: AES Key Decrypted Successfully</div><div class="step-desc">• Kunci Simetris Terpulihkan: <code style="font-size:0.75rem;">{trunc_aes_key}</code></div></div>'
                    step4.markdown(log_html, unsafe_allow_html=True)
                    logs["step4"] = log_html
                except Exception as e:
                    log_html = f'<div class="step-card step-failed"><div class="step-title" style="color:#ef4444;">❌ Step 4: Decryption of AES Key Failed</div><div class="step-desc">Passphrase salah atau format kunci privat tidak cocok! (Error: {str(e)})</div></div>'
                    step4.markdown(log_html, unsafe_allow_html=True)
                    logs["step4"] = log_html
                    st.session_state["recover_logs"] = logs
                    st.stop()

                # ----------------- STEP 5: FILE DECRYPTION (AES-256) -----------------
                step5.markdown(
                    '<div class="step-card">'
                    '<div class="step-title">📂 Step 5: Decrypting Source File with AES-256-CBC...</div>'
                    '<div class="step-desc">Mendekripsi berkas biner `.enc` secara chunked untuk memulihkan berkas data asli Anda secara utuh.</div>'
                    '</div>', 
                    unsafe_allow_html=True
                )
                time.sleep(1.0)

                try:
                    recovered_path = f"storage/decrypted/recovered_{metadata['filename']}"
                    aes_util.decrypt_file(temp_enc, recovered_path, aes_key)
                    
                    aes_key = None
                    
                    log_html = f'<div class="step-card step-success"><div class="step-title" style="color:#10b981;">✔️ Step 5: File Decrypted & Restored Successfully</div><div class="step-desc">• Path Penyimpanan Lokal: <code>{recovered_path}</code></div></div>'
                    step5.markdown(log_html, unsafe_allow_html=True)
                    logs["step5"] = log_html
                    
                    st.session_state["recover_logs"] = logs
                    st.session_state["recover_result"] = {
                        "recovered_file": recovered_path,
                        "filename": metadata["filename"]
                    }
                    
                    st.balloons()
                    st.rerun()
                except Exception as e:
                    log_html = f'<div class="step-card step-failed"><div class="step-title" style="color:#ef4444;">❌ Step 5: File Decryption Failed</div><div class="step-desc">{str(e)}</div></div>'
                    step5.markdown(log_html, unsafe_allow_html=True)
                    logs["step5"] = log_html
                    st.session_state["recover_logs"] = logs
                    st.stop()

        # Render persistent logs & download button if they exist in session state
        if "recover_logs" in st.session_state:
            logs = st.session_state["recover_logs"]
            for step_key in ["step1", "step2", "step3", "step4", "step5"]:
                if step_key in logs:
                    st.markdown(logs[step_key], unsafe_allow_html=True)
            
            if "recover_result" in st.session_state:
                result = st.session_state["recover_result"]
                st.success("🎉 Audit Keamanan & Pemulihan Berkas Berhasil 100%!")
                
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown('### 📥 Unduh Hasil Pemulihan Berkas', unsafe_allow_html=True)
                
                with open(result["recovered_file"], "rb") as f:
                    st.download_button(
                        label=f"Download Recovered: {result['filename']}",
                        data=f.read(),
                        file_name=result['filename'],
                        use_container_width=True,
                        key="btn_download_recovered"
                    )
        elif not recover_btn:
            st.info("💡 Masukkan berkas bahan pemulihan di kolom kiri lalu tekan tombol untuk memulai Audit Pemulihan.")

# ----------------- PAGE 4: BLOCKCHAIN EXPLORER -----------------
elif menu == "🔗 Blockchain Explorer":
    st.markdown('<h1 class="gradient-title">🔗 Blockchain Ledger Explorer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Buku kas terdistribusi pencatatan integritas hash berkas terenkripsi secara transparan dan anti-modifikasi</p>', unsafe_allow_html=True)

    chain = blockchain.load_blockchain()

    # Blockchain summary indicators
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown(f"**Total Blocks:** `{len(chain)}`")
    with cols[1]:
        is_valid = blockchain.verify_blockchain()
        val_badge = '<span class="status-badge badge-success">Sempurna / Valid</span>' if is_valid else '<span class="status-badge badge-danger">Rusak / Tampered</span>'
        st.markdown(f"**Integritas Rantai:** {val_badge}", unsafe_allow_html=True)
    with cols[2]:
        st.markdown("**Algoritma Hash Hubung:** `SHA-256`")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### ⛓️ Rantai Blok Terpelihara (Blok Terbaru di Bawah)", unsafe_allow_html=True)
    
    if len(chain) == 0:
        st.info("Belum ada blok yang dibuat. Silakan secure berkas terlebih dahulu untuk menambahkan transaksi.")
    else:
        for block in chain:
            # We determine the theme of genesis block vs transaction blocks
            is_genesis = block["file_hash"] == "GENESIS_BLOCK"
            border_color = "#10b981" if is_genesis else "#6366f1"
            bg_gradient = "linear-gradient(135deg, rgba(16,185,129,0.05) 0%, rgba(30,41,59,0.3) 100%)" if is_genesis else "linear-gradient(135deg, rgba(99,102,241,0.05) 0%, rgba(30,41,59,0.3) 100%)"
            
            block_html = f"""
            <div style="
                border: 1px solid rgba(255,255,255,0.08);
                border-left: 5px solid {border_color};
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 15px;
                background: {bg_gradient};
                backdrop-filter: blur(8px);
            ">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 10px;">
                    <span style="font-weight:800; font-size:1.15rem; color:{border_color};">BLOCK #{block['index']}</span>
                    <span style="font-size:0.8rem; color:#64748b;">⏳ Timestamp: {block['timestamp']}</span>
                </div>
                <div style="font-size:0.85rem; color:#475569; line-height: 1.8;">
                    <div style="margin-bottom:4px;"><b>📂 File SHA-256 Hash:</b> <code style="color:#34d399; font-size:0.78rem;">{block['file_hash']}</code></div>
                    <div style="margin-bottom:4px;"><b>🔗 Previous Block Hash:</b> <code style="color:#94a3b8; font-size:0.78rem;">{block['previous_hash']}</code></div>
                    <div><b>🔒 Current Block Hash:</b> <code style="color:#22d3ee; font-size:0.78rem;">{block['current_hash']}</code></div>
                </div>
            </div>
            """
            st.markdown(block_html, unsafe_allow_html=True)
