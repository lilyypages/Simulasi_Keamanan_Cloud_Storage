import os
import sys

# Add root project path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crypto.aes_util import generate_aes_key
from crypto.rsa_util import (
    generate_rsa_keys,
    encrypt_aes_key,
    decrypt_aes_key
)


def test_rsa_workflow():

    print("=== RSA TEST START ===")

    # Generate RSA keys
    generate_rsa_keys()

    # Generate AES key
    aes_key = generate_aes_key()
    print("[+] AES key generated")

    # Encrypt AES key
    encrypted_key = encrypt_aes_key(aes_key)
    print("[+] AES key encrypted with RSA")

    # Decrypt AES key
    decrypted_key = decrypt_aes_key(encrypted_key)
    print("[+] AES key decrypted")

    # Verify
    if aes_key == decrypted_key:
        print("[SUCCESS] RSA encryption & decryption successful")
    else:
        print("[FAILED] AES key mismatch")

    print("=== RSA TEST COMPLETE ===")


if __name__ == "__main__":
    test_rsa_workflow()