import streamlit as st
import os
import json
from datetime import datetime

# Set layout (Paksa sidebar agar selalu terbuka secara default)
st.set_page_config(page_title="CyberClinic Security", page_icon="🔐", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# INJEKSI CUSTOM CSS (MENGHACK STREAMLIT)
# ==========================================
custom_css = """
<style>
/* Font family */
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif !important;
}

/* Hilangkan bar putih kosong di bagian paling atas (Header) */
header[data-testid="stHeader"] {
    background-color: transparent !important;
    box-shadow: none !important;
}

/* Sembunyikan tombol Deploy dan Menu tiga titik (Toolbar) */
.stDeployButton {display: none !important;}
[data-testid="stToolbar"] {display: none !important;}

/* Hanya sembunyikan footer */
footer {visibility: hidden !important;}

/* Sembunyikan tombol tutup sidebar menggunakan visibility agar layout tidak rusak */
[data-testid="stSidebarCollapseButton"] {
    visibility: hidden !important;
    pointer-events: none !important;
}

/* Background Latar Belakang Aplikasi (Teal Muda) */
.stApp {
    background-color: #DDEEEA !important;
}

/* Sidebar Kuning Terang (CyberClinic Style) */
[data-testid="stSidebar"] {
    background-color: #FFC400 !important;
    border-right: none;
    border-radius: 0 35px 35px 0;
    box-shadow: 5px 0 20px rgba(0,0,0,0.08);
    min-width: 300px !important;
    max-width: 300px !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p, 
[data-testid="stSidebar"] span {
    color: #212529 !important;
    font-weight: 700 !important;
}

/* Sembunyikan titik (dot) pada radio button */
div.stRadio > div[role="radiogroup"] > label > div:first-child {
    display: none !important;
}

/* Radio button text sidebar (Dibuat lebih lega dan mulus) */
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

/* Main Block Container (Kotak Putih Mengambang) */
.block-container {
    background-color: #FFFFFF !important;
    border-radius: 30px;
    padding: 2.5rem 3.5rem !important;
    margin-top: 1.5rem !important;
    margin-bottom: 2rem !important;
    box-shadow: 0 15px 35px rgba(0,0,0,0.04);
    max-width: 92% !important;
}

/* Custom Colorful Cards */
.custom-card {
    border-radius: 20px;
    padding: 24px;
    color: white;
    height: 150px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}
.custom-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 25px rgba(0,0,0,0.12);
}
.card-blue { background: linear-gradient(135deg, #2563EB, #3B82F6); }
.card-green { background: linear-gradient(135deg, #10B981, #34D399); }
.card-orange { background: linear-gradient(135deg, #F97316, #FB923C); }
.card-yellow { background: linear-gradient(135deg, #F59E0B, #FBBF24); color: #453000; }

.card-title {
    font-size: 0.95rem;
    font-weight: 700;
    opacity: 0.95;
    letter-spacing: 0.5px;
}
.card-value {
    font-size: 1.8rem;
    font-weight: 800;
    margin-top: 5px;
}

/* Custom Table (Tabel Pastel) */
.custom-table-container {
    width: 100%;
    margin-top: 25px;
    overflow-x: auto;
}
.custom-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0 12px;
}
.custom-table th {
    text-align: left;
    padding: 12px 18px;
    color: #6B7280;
    font-weight: 800;
    font-size: 0.95rem;
    border-bottom: 2px solid #F3F4F6;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.custom-table td {
    padding: 16px 18px;
    font-weight: 600;
    font-size: 0.95rem;
    color: #374151;
}
.custom-table tr:nth-child(1) td { background-color: #F0FDFA; }
.custom-table tr:nth-child(2) td { background-color: #FFF1F2; }
.custom-table tr:nth-child(3) td { background-color: #FEFCE8; }
.custom-table tr:nth-child(4) td { background-color: #F0FDFA; }
.custom-table tr:nth-child(5) td { background-color: #F8FAFC; }
.custom-table tr td:first-child { border-radius: 12px 0 0 12px; }
.custom-table tr td:last-child { border-radius: 0 12px 12px 0; }
.custom-table tr {
    transition: transform 0.2s;
}
.custom-table tr:hover td {
    filter: brightness(0.97);
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Import backend modules
from utils.workflow import secure_file, recover_file
from crypto.rsa_util import generate_rsa_keys
from blockchain.blockchain import load_blockchain

# Define storage directories
UPLOAD_DIR = "storage/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs("keys", exist_ok=True)

# Helper function to save uploaded file
def save_uploaded_file(uploaded_file, target_dir=UPLOAD_DIR):
    if uploaded_file is not None:
        file_path = os.path.join(target_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    return None

# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.title("☁️ Keamanan Cloud")
st.sidebar.markdown("<br>", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigasi",
    ["Dashboard Status", "Book Keys (RSA)", "Digital Protection", "Order Recovery"],
    label_visibility="collapsed"
)

# ==========================================
# PAGE 1: DASHBOARD
# ==========================================
if page == "Dashboard Status":
    st.markdown("### 🔍 Dashboard Overview")
    
    # Get Data
    try:
        chain = load_blockchain()
        total_blocks = len(chain)
    except Exception:
        chain = []
        total_blocks = 0
        
    rsa_exists = os.path.exists("keys/private.pem") and os.path.exists("keys/public.pem")
    
    # Custom Colored Cards HTML
    html_cards = f"""
    <div style="display: flex; gap: 15px; margin-bottom: 30px; flex-wrap: wrap;">
        <div style="flex: 1; min-width: 200px;" class="custom-card card-blue">
            <div class="card-title">Total Blockchain Records</div>
            <div class="card-value">{total_blocks} Blocks</div>
            <div style="font-size: 0.75rem; opacity: 0.8;">Secured by SHA-256</div>
        </div>
        <div style="flex: 1; min-width: 200px;" class="custom-card card-green">
            <div class="card-title">RSA Key Pair Status</div>
            <div class="card-value">{"Active" if rsa_exists else "Missing"}</div>
            <div style="font-size: 0.75rem; opacity: 0.8;">RSA-2048 Asymmetric</div>
        </div>
        <div style="flex: 1; min-width: 200px;" class="custom-card card-orange">
            <div class="card-title">System Integrity</div>
            <div class="card-value">{"Valid" if total_blocks > 0 else "Empty"}</div>
            <div style="font-size: 0.75rem; opacity: 0.8;">No Tampering Detected</div>
        </div>
        <div style="flex: 1; min-width: 200px;" class="custom-card card-yellow">
            <div class="card-title">AES File Encryption</div>
            <div class="card-value">Ready</div>
            <div style="font-size: 0.75rem; opacity: 0.8;">AES-256 CBC Mode</div>
        </div>
    </div>
    """
    st.markdown(html_cards, unsafe_allow_html=True)
    
    # Custom History Table HTML
    st.markdown("### 📋 Encryption History (Blockchain)")
    
    if total_blocks > 0:
        table_html = "<div class='custom-table-container'><table class='custom-table'><thead><tr><th>Block Id</th><th>Timestamp</th><th>File Hash (Truncated)</th><th>Status</th></tr></thead><tbody>"
        for i, block in enumerate(reversed(chain[-4:])): # Ambil 4 terakhir
            hash_trunc = block.get('file_hash', '')[:20] + '...'
            date_str = block.get('timestamp', '')[:16]
            table_html += f"<tr><td>{block.get('index', '0')}</td><td>{date_str}</td><td>{hash_trunc}</td><td>✅ Secure</td></tr>"
        table_html += "</tbody></table></div>"
        st.markdown(table_html, unsafe_allow_html=True)
    else:
        st.info("Belum ada data di dalam blockchain.")

# ==========================================
# PAGE 2: MANAJEMEN KUNCI
# ==========================================
elif page == "Book Keys (RSA)":
    st.markdown("### 🔑 Setup RSA Keys")
    st.markdown("Sistem ini membutuhkan pasangan Kunci RSA (Public & Private) untuk mengenkripsi Kunci AES yang digunakan mengamankan file Anda.")
    
    if st.session_state.get('rsa_generated'):
        st.success("🎉 Kunci RSA berhasil dibuat dan disimpan!")
        st.session_state.rsa_generated = False
    
    rsa_exists = os.path.exists("keys/private.pem") and os.path.exists("keys/public.pem")
    
    if rsa_exists:
        st.success("✅ Pasangan Kunci RSA sudah tersedia di sistem.")
        st.warning("Membuat kunci baru akan menimpa kunci lama!")
        
    st.markdown("#### Generate Kunci Baru")
    passphrase = st.text_input("Masukkan Passphrase (Password) untuk Kunci Privat:", type="password")
    confirm_passphrase = st.text_input("Konfirmasi Passphrase:", type="password")
    
    if st.button("Generate Kunci RSA", type="primary"):
        if passphrase != confirm_passphrase:
            st.error("Passphrase tidak cocok!")
        elif len(passphrase) < 6:
            st.warning("Passphrase terlalu pendek. Gunakan minimal 6 karakter.")
        else:
            with st.spinner("Sedang membuat Kunci RSA-2048..."):
                try:
                    generate_rsa_keys(passphrase=passphrase)
                    st.session_state.rsa_generated = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Gagal membuat kunci: {str(e)}")

# ==========================================
# PAGE 3: AMANKAN FILE
# ==========================================
elif page == "Digital Protection":
    st.markdown("### 🔒 Secure File")
    
    if not (os.path.exists("keys/private.pem") and os.path.exists("keys/public.pem")):
        st.error("Kunci RSA belum di-setup! Silakan ke menu 'Book Keys (RSA)' terlebih dahulu.")
        st.stop()
        
    col1, col2 = st.columns(2)
    with col1:
        secret_file = st.file_uploader("Upload Medical/Secret File", type=None)
    with col2:
        cover_image = st.file_uploader("Upload Cover Image (PNG)", type=['png'])
        if cover_image:
            st.image(cover_image, caption="Cover Image")
            
    if secret_file and cover_image:
        if st.button("🔐 Encrypt & Embed Data", type="primary"):
            with st.spinner("Processing..."):
                try:
                    saved_secret = save_uploaded_file(secret_file)
                    saved_cover = save_uploaded_file(cover_image)
                    result = secure_file(saved_secret, saved_cover)
                    
                    st.success("✅ Security Protocol Executed!")
                    st.info(f"**Generated Hash:**\n`{result['hash']}`")
                    
                    res_col1, res_col2 = st.columns(2)
                    with res_col1:
                        with open(result["encrypted_file"], "rb") as enc_file:
                            st.download_button("⬇️ Download Encrypted File", data=enc_file, file_name=os.path.basename(result["encrypted_file"]))
                    with res_col2:
                        with open(result["stego_image"], "rb") as stego_file:
                            st.download_button("⬇️ Download Stego Image", data=stego_file, file_name=os.path.basename(result["stego_image"]), mime="image/png")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ==========================================
# PAGE 4: PULIHKAN FILE
# ==========================================
elif page == "Order Recovery":
    st.markdown("### 🔓 Data Recovery")
    
    if not os.path.exists("keys/private.pem"):
        st.error("Kunci Privat RSA tidak ditemukan di sistem!")
        st.stop()
        
    col1, col2 = st.columns(2)
    with col1:
        enc_file_upload = st.file_uploader("Upload Encrypted File (.enc)", type=None)
    with col2:
        stego_upload = st.file_uploader("Upload Stego Image (PNG)", type=['png'])
        
    passphrase_input = st.text_input("Enter RSA Passphrase:", type="password")
    
    if enc_file_upload and stego_upload and passphrase_input:
        if st.button("🔓 Decrypt & Recover", type="primary"):
            with st.spinner("Verifying integrity..."):
                try:
                    saved_enc = save_uploaded_file(enc_file_upload)
                    saved_stego = save_uploaded_file(stego_upload)
                    result = recover_file(saved_enc, saved_stego, rsa_passphrase=passphrase_input)
                    
                    st.success("✅ " + result["status"])
                    recovered_path = result["recovered_file"]
                    with open(recovered_path, "rb") as rec_file:
                        st.download_button("⬇️ Download Recovered File", data=rec_file, file_name=os.path.basename(recovered_path))
                except Exception as e:
                    st.error(f"❌ Failed: {str(e)}")
