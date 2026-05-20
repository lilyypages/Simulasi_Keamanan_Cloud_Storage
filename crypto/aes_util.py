import logging
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

logger = logging.getLogger(__name__)

CHUNK_SIZE = 64 * 1024  # 64 KB per chunk


def generate_aes_key():
    """Generate AES-256 key (32 bytes)."""
    return get_random_bytes(32)


def encrypt_file(input_path, output_path, key):
    """
    Encrypt file using AES-256 CBC with proper PKCS7 padding.
    Chunked mode implementation.
    """
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    with open(input_path, 'rb') as fin, open(output_path, 'wb') as fout:
        # Write IV first
        fout.write(iv)
        # Read first chunk
        chunk = fin.read(CHUNK_SIZE)
        while chunk:
            # Read next chunk to detect EOF
            next_chunk = fin.read(CHUNK_SIZE)
            # If this is final chunk → apply padding
            if len(next_chunk) == 0:
                chunk = pad(chunk, AES.block_size)
            encrypted_chunk = cipher.encrypt(chunk)
            fout.write(encrypted_chunk)
            chunk = next_chunk
    logger.info(f"File encrypted: {output_path}")
    return output_path


def decrypt_file(input_path, output_path, key):
    """Decrypt AES encrypted file with chunked reading."""
    with open(input_path, 'rb') as fin:
        iv = fin.read(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Read all encrypted chunks
        chunks = []
        while True:
            chunk = fin.read(CHUNK_SIZE)
            if not chunk:
                break
            chunks.append(chunk)

    # Decrypt and write output
    with open(output_path, 'wb') as fout:
        for i, chunk in enumerate(chunks):
            decrypted_chunk = cipher.decrypt(chunk)
            if i == len(chunks) - 1:
                # Last chunk — remove padding
                decrypted_chunk = unpad(decrypted_chunk, AES.block_size)
            fout.write(decrypted_chunk)

    logger.info(f"File decrypted: {output_path}")
    return output_path
