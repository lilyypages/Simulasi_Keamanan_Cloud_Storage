from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


# Generate AES-256 key (32 bytes)
def generate_aes_key():
    return get_random_bytes(32)


# Encrypt file using AES-256 CBC
def encrypt_file(input_path, output_path, key):

    # Read original file
    with open(input_path, 'rb') as f:
        plaintext = f.read()

    # Generate random IV
    iv = get_random_bytes(16)

    # Create AES cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Encrypt with padding
    ciphertext = cipher.encrypt(
        pad(plaintext, AES.block_size)
    )

    # Save IV + ciphertext
    with open(output_path, 'wb') as f:
        f.write(iv + ciphertext)

    return output_path


# Decrypt AES encrypted file
def decrypt_file(input_path, output_path, key):

    # Read encrypted file
    with open(input_path, 'rb') as f:

        # First 16 bytes = IV
        iv = f.read(16)

        # Remaining bytes = ciphertext
        ciphertext = f.read()

    # Create AES cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt and remove padding
    plaintext = unpad(
        cipher.decrypt(ciphertext),
        AES.block_size
    )

    # Save decrypted file
    with open(output_path, 'wb') as f:
        f.write(plaintext)

    return output_path