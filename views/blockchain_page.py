# views/blockchain_page.py
import streamlit as st
from blockchain import blockchain

def render_blockchain_explorer():
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
            border_color = "#10b981" if is_genesis else "#4f46e5"
            bg_gradient = "linear-gradient(135deg, rgba(16,185,129,0.08) 0%, #ffffff 100%)" if is_genesis else "linear-gradient(135deg, rgba(79,102,241,0.05) 0%, #ffffff 100%)"
            
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
                <div style="font-size:0.85rem; color:#cbd5e1; line-height: 1.8;">
                    <div style="margin-bottom:4px;"><b>📂 File SHA-256 Hash:</b> <code style="color:#34d399; font-size:0.78rem;">{block['file_hash']}</code></div>
                    <div style="margin-bottom:4px;"><b>🔗 Previous Block Hash:</b> <code style="color:#94a3b8; font-size:0.78rem;">{block['previous_hash']}</code></div>
                    <div><b>🔒 Current Block Hash:</b> <code style="color:#22d3ee; font-size:0.78rem;">{block['current_hash']}</code></div>
                </div>
            </div>
            """
            st.markdown(block_html, unsafe_allow_html=True)