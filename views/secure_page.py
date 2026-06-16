# views/secure_page.py
import os
import time
import streamlit as st
from utils.workflow import secure_file

def render_secure_file(clear_temp_func):
    st.markdown('<h1 class="gradient-title">🔒 Secure & Encrypt File</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Lakukan pengamanan data berlapis: enkripsi data, pasang blockchain hash, dan sisipkan metadata ke gambar stego</p>', unsafe_allow_html=True)

    # Check RSA keys
    if not os.path.exists("keys/public.pem"):
        st.warning("⚠️ Kunci publik RSA tidak terdeteksi. Silakan buat Key Pair terlebih dahulu di Dashboard!")
    else:
        left, right = st.columns([1, 1])

        with left:
            st.markdown('<h4 style="color:#a5b4fc;">Upload Berkas & Cover</h4>', unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader("Upload File Sensitif (Apapun)", type=None)
            
            use_default_cover = st.checkbox("Gunakan gambar cover default (assets/cover.png)", value=True)
            
            uploaded_cover = None
            if not use_default_cover:
                uploaded_cover = st.file_uploader("Upload Gambar Cover Kustom (PNG)", type=["png"])

        with right:
            st.markdown('<h4 style="color:#a5b4fc;">Konfigurasi Keamanan</h4>', unsafe_allow_html=True)
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
                    clear_temp_func()  # Panggil fungsi clear_temp dari app.py
                    
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