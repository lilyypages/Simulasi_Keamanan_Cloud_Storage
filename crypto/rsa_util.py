from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# Generate RSA key pair
def generate_rsa_keys(
    private_key_path="keys/private.pem",
    public_key_path="keys/public.pem"
):

    # Generate 2048-bit RSA key
    key = RSA.generate(2048)

    # Export private key
    private_key = key.export_key()

    # Export public key
    public_key = key.publickey().export_key()

    # Save private key
    with open(private_key_path, 'wb') as f:
        f.write(private_key)

    # Save public key
    with open(public_key_path, 'wb') as f:
        f.write(public_key)

    print("[+] RSA key pair generated")


# Encrypt AES key using RSA public key
def encrypt_aes_key(aes_key, public_key_path="keys/public.pem"):

    # Load public key
    with open(public_key_path, 'rb') as f:
        public_key = RSA.import_key(f.read())

    # Create cipher
    cipher_rsa = PKCS1_OAEP.new(public_key)

    # Encrypt AES key
    encrypted_key = cipher_rsa.encrypt(aes_key)

    return base64.b64encode(encrypted_key).decode()


# Decrypt AES key using RSA private key
def decrypt_aes_key(encrypted_key, private_key_path="keys/private.pem"):

    # Load private key
    with open(private_key_path, 'rb') as f:
        private_key = RSA.import_key(f.read())

    # Create cipher
    cipher_rsa = PKCS1_OAEP.new(private_key)

    # Decrypt AES key
    encrypted_key = base64.b64decode(encrypted_key)

    decrypted_key = cipher_rsa.decrypt(encrypted_key)

    return decrypted_key