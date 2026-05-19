import os
import sys

# Tambahkan root project ke path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crypto.aes_util import (
    generate_aes_key,
    encrypt_file,
    decrypt_file
)

# Path file
INPUT_FILE = "storage/uploads/sample.txt"
ENCRYPTED_FILE = "storage/encrypted/sample.enc"
DECRYPTED_FILE = "storage/decrypted/sample_decrypted.txt"


def test_aes_workflow():

    print("=== AES TEST START ===")

    # Generate AES-256 key
    key = generate_aes_key()
    print("[+] AES key generated")

    # Encrypt file
    encrypt_file(INPUT_FILE, ENCRYPTED_FILE, key)
    print("[+] File encrypted")

    # Decrypt file
    decrypt_file(ENCRYPTED_FILE, DECRYPTED_FILE, key)
    print("[+] File decrypted")

    # Read original file
    with open(INPUT_FILE, 'rb') as f:
        original_data = f.read()

    # Read decrypted file
    with open(DECRYPTED_FILE, 'rb') as f:
        decrypted_data = f.read()

    # Compare content
    if original_data == decrypted_data:
        print("[SUCCESS] AES encryption & decryption successful")
    else:
        print("[FAILED] File mismatch detected")

    print("=== AES TEST COMPLETE ===")


if __name__ == "__main__":
    test_aes_workflow()