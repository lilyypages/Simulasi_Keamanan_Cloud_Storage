import os
import sys

# Add root project path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crypto.hash_util import (
    generate_file_hash,
    verify_file_hash
)


TEST_FILE = "storage/uploads/sample.txt"


def test_hash_workflow():

    print("=== HASH TEST START ===")

    # Generate hash
    file_hash = generate_file_hash(TEST_FILE)

    print("[+] SHA-256 hash generated")
    print(f"Hash: {file_hash}")

    # Verify hash
    is_valid = verify_file_hash(TEST_FILE, file_hash)

    if is_valid:
        print("[SUCCESS] Hash verification successful")
    else:
        print("[FAILED] Hash verification failed")

    print("=== HASH TEST COMPLETE ===")


if __name__ == "__main__":
    test_hash_workflow()