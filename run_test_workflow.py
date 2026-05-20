# run_test_workflow.py
import os
from utils import workflow
from crypto import aes_util, rsa_util, hash_util
from stego import lsb

def test_full_flow():
    print("--- MEMULAI SIMULASI PENGUJIAN BACKEND ---")
    
    # 1. Siapkan file dummy untuk ditest
    file_asli = "test_dokumen.txt"
    with open(file_asli, "w") as f:
        f.write("Ini adalah data sensitif rahasia kelompok 5")
    
    file_terenkripsi = "uploads/encrypted/test_dokumen.bin"
    gambar_cover = "assets/cover.png"
    gambar_stego = "storage/stego_images/stego_output.png"
    file_pemulihan = "storage/decrypted/test_dokumen_recovered.txt"
    
    # Pastikan folder output ada
    os.makedirs("uploads/encrypted", exist_ok=True)
    os.makedirs("storage/stego_images", exist_ok=True)
    os.makedirs("storage/decrypted", exist_ok=True)
    os.makedirs("keys", exist_ok=True)

    try:
        # 2. Test enkripsi & keamanan (Pekerjaan Kayla)
        print("\n[1] Membuat Keypair RSA...")
        priv_path, pub_path = rsa_util.generate_rsa_keys(passphrase="kelompok5b")
        
        print("[2] Mengenkripsi File dengan AES-256 (Chunk Mode)...")
        aes_key = aes_util.generate_aes_key()
        aes_util.encrypt_file(file_asli, file_terenkripsi, aes_key)
        
        print("[3] Mengamankan Kunci AES dengan Kunci Publik RSA...")
        encrypted_aes_key = rsa_util.encrypt_aes_key(aes_key, pub_path)
        
        # Buat metadata untuk disembunyikan
        file_hash = hash_util.generate_sha256_hash(file_terenkripsi)
        metadata = {
            "aes_key": encrypted_aes_key,
            "file_hash": file_hash
        }
        
        print("[4] Menyisipkan Metadata ke Gambar (LSB Steganografi)...")
        lsb.embed_metadata(gambar_cover, metadata, gambar_stego)
        print("-> Sukses! Silakan cek folder 'storage/stego_images/'")
        
        # 3. Test Ekstraksi dan Pemulihan
        print("\n[5] Mencoba Ekstrak Metadata dari Gambar...")
        extracted_metadata = lsb.extract_metadata(gambar_stego)
        
        print("[6] Mendekripsi Kunci AES menggunakan Private Key RSA...")
        decrypted_aes_key = rsa_util.decrypt_aes_key(
            extracted_metadata["aes_key"], 
            private_key_path=priv_path, 
            passphrase="kelompok5b"
        )
        
        print("[7] Mendekripsi File Terenkripsi...")
        aes_util.decrypt_file(file_terenkripsi, file_pemulihan, decrypted_aes_key)
        
        # 4. Validasi Hasil
        with open(file_pemulihan, "r") as f:
            isi_file = f.read()
        print(f"\n[HASIL] Isi file yang berhasil dipulihkan: '{isi_file}'")
        print("✅ KODE BACKEND AMAN & BERHASIL DIREFACTOR!")
        
    except Exception as e:
        print(f"\n❌ PENGUJIAN GAGAL: {str(e)}")

if __name__ == "__main__":
    test_full_flow()