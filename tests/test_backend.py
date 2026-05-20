import os
import sys

# Tambahkan root project ke path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

from crypto import (aes_util,rsa_util,hash_util)
from stego import lsb
from blockchain.blockchain import (add_block,verify_blockchain)

def test_backend():
    print("=== BACKEND SECURITY TEST START ===")
    # Prepare directories
    os.makedirs("storage/uploads",exist_ok=True)
    os.makedirs("storage/encrypted",exist_ok=True)
    os.makedirs("storage/stego_images", exist_ok=True)
    os.makedirs("storage/decrypted",exist_ok=True)
    os.makedirs("keys",exist_ok=True)
    # File paths
    file_asli = ("storage/uploads/test_dokumen.txt")
    file_terenkripsi = ("storage/encrypted/test_dokumen.enc")
    gambar_cover = "assets/cover.png"
    gambar_stego = ("storage/stego_images/"
                    "stego_output.png")
    file_pemulihan = ("storage/decrypted/"
                      "test_dokumen_recovered.txt")
    # Create sample file
    with open(file_asli, "w") as f:
        f.write(
            "Ini adalah data sensitif "
            "rahasia kelompok 5"
        )
    try:
        # RSA KEY GENERATION
        print("\n[1] Membuat RSA Key Pair...")
        priv_path, pub_path = (
            rsa_util.generate_rsa_keys(
                passphrase="kelompok5b"
            )
        )
        print("[SUCCESS] RSA keypair created")
        # AES ENCRYPTION
        print(
            "\n[2] Mengenkripsi File "
            "dengan AES-256..."
        )
        aes_key = (aes_util.generate_aes_key())
        aes_util.encrypt_file(file_asli,
                              file_terenkripsi,
                              aes_key)
        print("[SUCCESS] File encrypted")
        # RSA AES KEY ENCRYPTION
        print(
            "\n[3] Mengenkripsi AES Key "
            "dengan RSA..."
        )
        encrypted_aes_key = (
            rsa_util.encrypt_aes_key(aes_key,pub_path))
        print("[SUCCESS] AES key protected")
        # SHA256 HASHING
        print("\n[4] Membuat SHA256 Hash..."
        )
        file_hash = (
            hash_util.generate_file_hash(
                file_terenkripsi
            )
        )
        print("[SUCCESS] Hash generated")
        print(file_hash)
        # BLOCKCHAIN
        print(
            "\n[5] Menyimpan Hash "
            "ke Blockchain..."
        )
        add_block(file_hash)
        blockchain_valid = (
            verify_blockchain()
        )
        if blockchain_valid:
            print("[SUCCESS] Blockchain valid")
        else:
            raise Exception("Blockchain verification failed")
        # STEGANOGRAPHY
        print(
            "\n[6] Menyisipkan Metadata "
            "ke Gambar..."
        )
        metadata = {
            "filename": "test_dokumen.txt",
            "encrypted_key": encrypted_aes_key,
            "hash": file_hash
        }
        lsb.embed_metadata(gambar_cover,metadata,gambar_stego)
        print("[SUCCESS] Metadata embedded")
        # EXTRACT METADATA
        print("\n[7] Mengekstrak Metadata...")
        extracted_metadata = (
            lsb.extract_metadata(
                gambar_stego
            )
        )
        print("[SUCCESS] Metadata extracted")
        # HASH VERIFICATION
        print(
            "\n[8] Verifikasi Integritas "
            "File..."
        )
        hash_valid = (
            hash_util.verify_file_hash(
                file_terenkripsi,
                extracted_metadata["hash"]
            )
        )
        if not hash_valid:
            raise Exception(
                "Hash verification failed"
            )
        print("[SUCCESS] File integrity valid")
        # RSA DECRYPT AES KEY
        print("\n[9] Mendekripsi AES Key...")
        decrypted_aes_key = (
            rsa_util.decrypt_aes_key(
                extracted_metadata[
                    "encrypted_key"
                ],
                private_key_path=priv_path,
                passphrase="kelompok5b"
            )
        )
        print("[SUCCESS] AES key decrypted")

        # AES FILE DECRYPTION
        print("\n[10] Mendekripsi File...")
        aes_util.decrypt_file(
            file_terenkripsi,
            file_pemulihan,
            decrypted_aes_key
        )
        print("[SUCCESS] File recovered")
        # FINAL VALIDATION
        with open(
            file_pemulihan,
            "r"
        ) as f:
            isi_file = f.read()
        print("\n[RECOVERED CONTENT]")
        print(isi_file)
        print(
            "\n=== BACKEND TEST SUCCESSFUL ==="
        )
    except Exception as e:
        print(f"\n[FAILED] {str(e)}")
if __name__ == "__main__":
    test_backend()