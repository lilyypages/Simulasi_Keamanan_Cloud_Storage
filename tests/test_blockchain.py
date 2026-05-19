import os
import sys

# Add root project path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from blockchain.blockchain import (
    create_genesis_block,
    add_block,
    verify_blockchain
)

from crypto.hash_util import generate_file_hash


TEST_FILE = "storage/encrypted/sample.enc"


def test_blockchain_workflow():

    print("=== BLOCKCHAIN TEST START ===")

    # Create genesis block
    create_genesis_block()

    # Generate file hash
    file_hash = generate_file_hash(TEST_FILE)

    print("[+] File hash generated")

    # Add block
    block = add_block(file_hash)

    print("[+] Block added")
    print(block)

    # Verify blockchain
    is_valid = verify_blockchain()

    if is_valid:
        print("[SUCCESS] Blockchain verification successful")
    else:
        print("[FAILED] Blockchain corrupted")

    print("=== BLOCKCHAIN TEST COMPLETE ===")


if __name__ == "__main__":
    test_blockchain_workflow()