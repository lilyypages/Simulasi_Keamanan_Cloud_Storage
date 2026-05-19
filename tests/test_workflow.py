import os
import sys

# Add root project path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.workflow import (
    secure_file,
    recover_file
)


INPUT_FILE = "storage/uploads/sample.txt"

COVER_IMAGE = "assets/cover.png"


def test_full_workflow():

    print("=== FULL WORKFLOW TEST START ===")

    # Secure file
    result = secure_file(
        INPUT_FILE,
        COVER_IMAGE
    )

    print("[+] Secure file process complete")

    print(result)

    # Recover file
    recovery = recover_file(
        result["encrypted_file"],
        result["stego_image"]
    )

    print("[+] Recovery process complete")

    print(recovery)

    print("=== FULL WORKFLOW TEST COMPLETE ===")


if __name__ == "__main__":
    test_full_workflow()