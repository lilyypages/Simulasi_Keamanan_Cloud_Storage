import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from utils.workflow import (secure_file,recover_file)

def test_workflow():
    print("=== FULL WORKFLOW TEST START ===")
    os.makedirs("storage/uploads",exist_ok=True)
    test_file = ("storage/uploads/workflow_test.txt")

    with open(test_file, "w") as f:
        f.write(
            "Ini adalah simulasi "
            "workflow secure cloud storage"
        )
    cover_image = "assets/cover.png"

    try:
        # SECURE FILE PROCESS
        print("\n[1] Menjalankan Secure File...")
        secure_result = secure_file(
            test_file,
            cover_image
        )
        print("[SUCCESS] File secured")
        print("\n[SECURE RESULT]")
        print(secure_result)

        # RECOVER FILE PROCESS
        print("\n[2] Menjalankan Recovery...")
        recovery_result = recover_file(
            secure_result["encrypted_file"],
            secure_result["stego_image"],
            rsa_passphrase="kelompok5b"
        )
        print(
            "[SUCCESS] File recovered"
        )
        print("\n[RECOVERY RESULT]")
        print(recovery_result)
        
        # VALIDASI HASIL
        with open(
            recovery_result["recovered_file"],
            "r"
        ) as f:
            recovered_content = f.read()
        print("\n[RECOVERED CONTENT]")
        print(recovered_content)
        print("\n=== WORKFLOW TEST SUCCESSFUL ===")
    except Exception as e:
        print(
            f"\n[FAILED] {str(e)}"
        )

if __name__ == "__main__":
    test_workflow()