# views/dashboard_page.py
import os
import streamlit as st
from crypto import rsa_util

def render_dashboard():
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
        enc_count = len([f for f in os.listdir("storage/encrypted") if f.endswith(".enc")]) if os.path.exists("storage/encrypted") else 0
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
        st.markdown('<h3 style="color:#92c0fc; font-weight:700;">🔄 Alur Keamanan Multilayer</h3>', unsafe_allow_html=True)
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
        st.markdown('<h3 style="color:#92c0fc; font-weight:700;">🔑 Manajemen Kunci RSA</h3>', unsafe_allow_html=True)
        
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