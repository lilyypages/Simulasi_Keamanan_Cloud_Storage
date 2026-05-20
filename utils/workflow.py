import os
import logging

from crypto.aes_util import generate_aes_key, encrypt_file, decrypt_file
from crypto.rsa_util import encrypt_aes_key, decrypt_aes_key
from crypto.hash_util import generate_file_hash, verify_file_hash
from blockchain.blockchain import add_block, verify_blockchain
from stego.lsb import embed_metadata, extract_metadata

logger = logging.getLogger(__name__)


def secure_file(file_path, cover_image_path):
    os.makedirs("storage/encrypted", exist_ok=True)
    os.makedirs("storage/stego_images", exist_ok=True)
    
    filename = os.path.basename(file_path)
    encrypted_file_path = f"storage/encrypted/{filename}.enc"
    stego_output_path = f"storage/stego_images/{filename}_stego.png"

    # 1. Generate AES key
    aes_key = generate_aes_key()

    # 2. Encrypt file
    encrypt_file(file_path, encrypted_file_path, aes_key)

    # 3. Encrypt AES key with RSA
    encrypted_aes_key = encrypt_aes_key(aes_key)

    # 4. Generate SHA-256 hash of encrypted file
    file_hash = generate_file_hash(encrypted_file_path)

    # 5. Save hash to blockchain
    add_block(file_hash)

    # 6. Create metadata
    metadata = {
        "filename": filename,
        "encrypted_key": encrypted_aes_key,
        "hash": file_hash
    }

    # 7. Embed metadata into image
    embed_metadata(cover_image_path, metadata, stego_output_path)

    # 8. Clear AES key from local variable
    aes_key = None

    logger.info(f"File secured: {filename}")

    return {
        "encrypted_file": encrypted_file_path,
        "stego_image": stego_output_path,
        "hash": file_hash
    }


def recover_file(encrypted_file_path, stego_image_path, rsa_passphrase=None):
    """Recover file workflow: extract metadata, verify, decrypt."""
    os.makedirs("storage/decrypted", exist_ok=True)

    # 1. Extract metadata from stego image
    metadata = extract_metadata(stego_image_path)

    if metadata is None:
        raise Exception("Metadata extraction failed")

    encrypted_aes_key = metadata["encrypted_key"]
    original_hash = metadata["hash"]
    filename = metadata["filename"]


    # 2. Verify file integrity

    if not verify_blockchain():
        raise Exception("Blockchain verification failed — file may be tampered")
    
    # hash
    is_valid = verify_file_hash(encrypted_file_path, original_hash)

    if not is_valid:
        raise Exception("File integrity verification failed — file may have been tampered")

    # 3. Decrypt AES key using RSA private key
    aes_key = decrypt_aes_key(encrypted_aes_key, passphrase=rsa_passphrase)

    # 4. Recover original file
    recovered_file_path = f"storage/decrypted/recovered_{filename}"
    decrypt_file(encrypted_file_path, recovered_file_path, aes_key)

    # 5. Clear AES key from local variable
    aes_key = None

    logger.info(f"File recovered: {filename}")

    return {
        "recovered_file": recovered_file_path,
        "status": "Recovery successful"
    }
