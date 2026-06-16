# views/recover_page.py
import os
import time
import streamlit as st

# Import utility yang dibutuhkan oleh proses audit
from crypto import aes_util, rsa_util, hash_util
from stego import lsb
from blockchain import blockchain

def render_recover_file(clear_temp_func):
    st.markdown('<h1 class="gradient-title">🔑 Decrypt & Recover File</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Gunakan saluran audit interaktif untuk mengekstrak stego, memvalidasi integritas blockchain, mencocokkan SHA-256, dan memulihkan file asli</p>', unsafe_allow_html=True)

    col_inputs, col_audit = st.columns([2, 3])

    with col_inputs:
        st.markdown('<h3 style="color:#a5b4fc; font-size:1.3rem; font-weight:700;">📂 Input Bahan Pemulihan</h3>', unsafe_allow_html=True)
        
        stego_upload = st.file_uploader("1. Unggah Gambar Stego (PNG)", type=["png"])
        enc_upload = st.file_uploader("2. Unggah Berkas Terenkripsi (.enc)", type=["enc"])
        
        st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
        
        # Penomoran disesuaikan langsung ke input Passphrase, opsi RSA sudah otomatis di background
        passphrase_input = st.text_input("3. Passphrase Kunci Privat", type="password", help="Passphrase yang digunakan saat generate key pair")

        st.markdown('<div style="height:15px;"></div>', unsafe_allow_html=True)
        
        # Trigger button
        recover_btn = st.button("🚀 Start Deep Recovery Audit", use_container_width=True)

    with col_audit:
        st.markdown('<h3 style="color:#a5b4fc; font-size:1.3rem; font-weight:700;">🔍 Diagnostic Security Audit Logs</h3>', unsafe_allow_html=True)
        
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
            else:
                clear_temp_func() # Memanggil fungsi bawaan app.py yang di-passing

                # Save uploaded assets to temp files
                temp_stego = f"storage/temp/stego_{stego_upload.name}"
                with open(temp_stego, "wb") as f:
                    f.write(stego_upload.getbuffer())

                temp_enc = f"storage/temp/enc_{enc_upload.name}"
                with open(temp_enc, "wb") as f:
                    f.write(enc_upload.getbuffer())

                # Otomatis diarahkan langsung menggunakan kunci lokal sistem
                private_key_path = "keys/private.pem"
                
                # Check private key existence
                if not os.path.exists(private_key_path):
                    st.error("Kesalahan: Kunci privat RSA tidak ditemukan. Silakan cek folder keys/ atau buat Key Pair terlebih dahulu di Dashboard.")
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

        # Pemanggilan log persisten & tombol unduh
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