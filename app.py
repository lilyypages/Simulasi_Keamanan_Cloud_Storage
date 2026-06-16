# app.py
import os
import sys
import shutil
import streamlit as st

# Ensure project root is in the system path for imports
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from blockchain import blockchain
# Import halaman dashboard yang baru saja dipisahkan
from views.dashboard_page import render_dashboard 
from views.secure_page import render_secure_file
from views.recover_page import render_recover_file
from views.blockchain_page import render_blockchain_explorer

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

# Fungsi untuk load CSS dari file eksternal
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Jalankan fungsi untuk menyuntikkan CSS ke aplikasi
if os.path.exists("styles.css"):
    local_css("styles.css")
else:
    st.error("Berkas styles.css tidak ditemukan!")

# Helper function to clear temp files
def clear_temp():
    if os.path.exists("storage/temp"):
        shutil.rmtree("storage/temp")
    os.makedirs("storage/temp", exist_ok=True)

# Navigation setup
st.sidebar.markdown(
    '<div style="text-align: center; padding: 10px 0;">'
    '<h1 style="color: #818cf8; font-size: 1.6rem; font-weight: 800; margin-bottom: 0;">🛡️ STEGO-GUARD</h1>'
    '<p style="color: #64748b; font-size: 0.85rem; margin-top: 4px;">Multilayer Cloud Simulator</p>'
    '</div>',
    unsafe_allow_html=True
)

st.sidebar.markdown('<div class="divider"></div>', unsafe_allow_html=True)

menu = st.sidebar.radio(
    "NAVIGATION MENU",
    ["📊 Dashboard Overview", "🔒 Secure File Page", "🔑 Recover File Page", "🔗 Blockchain Explorer"],
    index=0
)

st.sidebar.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Sidebar system status widget
chain_valid = blockchain.verify_blockchain()
chain_len = len(blockchain.load_blockchain())

st.sidebar.markdown('<p style="font-weight:600; color:#94a3b8; font-size:0.8rem; margin-bottom:8px;">SYSTEM STATUS</p>', unsafe_allow_html=True)
if chain_valid:
    st.sidebar.markdown('<span class="status-badge badge-success">● Blockchain Secured</span>', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<span class="status-badge badge-danger">● Blockchain Corrupted</span>', unsafe_allow_html=True)

st.sidebar.markdown(f'<p style="font-size:0.85rem; color:#64748b; margin-top:8px;">Ledger Height: <b>{chain_len} Blocks</b></p>', unsafe_allow_html=True)

# ----------------- ROUTING MENUS -----------------
if menu == "📊 Dashboard Overview":
    render_dashboard() # Berubah jadi ringkas panggil fungsi dari file sebelah!

elif menu == "🔒 Secure File Page":
    render_secure_file(clear_temp_func=clear_temp)

elif menu == "🔑 Recover File Page":
    render_recover_file(clear_temp_func=clear_temp)

elif menu == "🔗 Blockchain Explorer":
    render_blockchain_explorer()