import os
import sys

# Add root project path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from stego.lsb import (
    embed_metadata,
    extract_metadata
)


IMAGE_PATH = "assets/cover.png"

OUTPUT_IMAGE = "storage/stego_images/stego.png"


metadata = {
    "filename": "sample.enc",
    "encrypted_key": "AES_KEY_RSA_ENCRYPTED",
    "hash": "SHA256_HASH"
}


def test_stego_workflow():

    print("=== STEGO TEST START ===")

    # Embed metadata
    embed_metadata(
        IMAGE_PATH,
        metadata,
        OUTPUT_IMAGE
    )

    # Extract metadata
    extracted = extract_metadata(
        OUTPUT_IMAGE
    )

    print("[+] Extracted Metadata:")
    print(extracted)

    # Verify
    if extracted == metadata:
        print("[SUCCESS] Steganography successful")
    else:
        print("[FAILED] Metadata mismatch")

    print("=== STEGO TEST COMPLETE ===")


if __name__ == "__main__":
    test_stego_workflow()