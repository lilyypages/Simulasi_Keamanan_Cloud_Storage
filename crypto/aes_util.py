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
    """Encrypt file using AES-256 CBC with chunked reading."""
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    with open(input_path, 'rb') as fin, open(output_path, 'wb') as fout:
        fout.write(iv)

        while True:
            chunk = fin.read(CHUNK_SIZE)
            if len(chunk) == 0:
                break
            elif len(chunk) % AES.block_size != 0:
                # Last chunk — apply padding
                chunk = pad(chunk, AES.block_size)
            fout.write(cipher.encrypt(chunk))

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
            decrypted = cipher.decrypt(chunk)
            if i == len(chunks) - 1:
                # Last chunk — remove padding
                decrypted = unpad(decrypted, AES.block_size)
            fout.write(decrypted)

    logger.info(f"File decrypted: {output_path}")
    return output_path
