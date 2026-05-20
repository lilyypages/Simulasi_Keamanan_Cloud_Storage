import os
import sys

# Add root project path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)

from crypto.aes_util import (
    generate_aes_key,
    encrypt_file,
    decrypt_file
)

# Directories
UPLOAD_DIR = "storage/uploads"
ENCRYPTED_DIR = "storage/encrypted"
DECRYPTED_DIR = "storage/decrypted"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(ENCRYPTED_DIR, exist_ok=True)
os.makedirs(DECRYPTED_DIR, exist_ok=True)


def run_aes_test(test_name, content):

    print(f"\n=== TEST: {test_name} ===")

    input_file = f"{UPLOAD_DIR}/{test_name}.txt"
    encrypted_file = f"{ENCRYPTED_DIR}/{test_name}.enc"
    decrypted_file = f"{DECRYPTED_DIR}/{test_name}_decrypted.txt"

    # Create test file
    with open(input_file, 'wb') as f:
        f.write(content)

    # Generate AES key
    key = generate_aes_key()

    # Encrypt
    encrypt_file(
        input_file,
        encrypted_file,
        key
    )

    print("[+] File encrypted")

    # Decrypt
    decrypt_file(
        encrypted_file,
        decrypted_file,
        key
    )

    print("[+] File decrypted")

    # Compare original vs decrypted
    with open(input_file, 'rb') as f:
        original_data = f.read()

    with open(decrypted_file, 'rb') as f:
        decrypted_data = f.read()

    if original_data == decrypted_data:
        print("[SUCCESS] AES test passed")
    else:
        print("[FAILED] AES mismatch detected")


def test_aes_workflow():

    print("=== AES TEST START ===")

    # Normal text
    run_aes_test(
        "normal_text",
        b"Hello Secure Cloud Storage"
    )

    # Exact AES block size (16 bytes)
    run_aes_test(
        "16_bytes",
        b"A" * 16
    )

    # Multiple AES blocks (32 bytes)
    run_aes_test(
        "32_bytes",
        b"B" * 32
    )

    # Larger file
    run_aes_test(
        "large_file",
        b"C" * 100000
    )

    # Empty file
    run_aes_test(
        "empty_file",
        b""
    )

    print("\n=== AES TEST COMPLETE ===")


if __name__ == "__main__":
    test_aes_workflow()