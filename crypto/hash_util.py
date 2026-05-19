import hashlib


# Generate SHA-256 hash from file
def generate_file_hash(file_path):

    sha256 = hashlib.sha256()

    # Read file in chunks
    with open(file_path, 'rb') as f:

        while True:
            chunk = f.read(4096)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()


# Verify file hash
def verify_file_hash(file_path, original_hash):

    current_hash = generate_file_hash(file_path)

    return current_hash == original_hash