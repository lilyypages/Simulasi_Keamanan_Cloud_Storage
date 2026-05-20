import logging
import os
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

logger = logging.getLogger(__name__)


def generate_rsa_keys(
    private_key_path="keys/private.pem",
    public_key_path="keys/public.pem",
    passphrase=None
):
    """Generate RSA-2048 key pair with optional passphrase protection."""
    key = RSA.generate(2048)

    # Export private key (encrypted if passphrase provided)
    private_key = key.export_key(passphrase=passphrase)
    public_key = key.publickey().export_key()

    # Ensure directories exist
    os.makedirs(os.path.dirname(private_key_path), exist_ok=True)
    os.makedirs(os.path.dirname(public_key_path), exist_ok=True)

    with open(private_key_path, 'wb') as f:
        f.write(private_key)

    with open(public_key_path, 'wb') as f:
        f.write(public_key)

    logger.info("RSA key pair generated")
    return private_key_path, public_key_path


def encrypt_aes_key(aes_key, public_key_path="keys/public.pem"):
    """Encrypt AES key using RSA public key."""
    with open(public_key_path, 'rb') as f:
        public_key = RSA.import_key(f.read())

    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_key = cipher_rsa.encrypt(aes_key)

    return base64.b64encode(encrypted_key).decode()


def decrypt_aes_key(encrypted_key_b64, private_key_path="keys/private.pem", passphrase=None):
    """Decrypt AES key using RSA private key."""
    with open(private_key_path, 'rb') as f:
        private_key = RSA.import_key(f.read(), passphrase=passphrase)

    cipher_rsa = PKCS1_OAEP.new(private_key)
    encrypted_key = base64.b64decode(encrypted_key_b64)

    return cipher_rsa.decrypt(encrypted_key)
