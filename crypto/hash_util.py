import hashlib


def generate_file_hash(file_path):
    """Generate SHA-256 hash from file using chunked reading."""
    sha256 = hashlib.sha256()

    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


def verify_file_hash(file_path, original_hash):
    """Verify file hash matches the original."""
    current_hash = generate_file_hash(file_path)
    return current_hash == original_hash


# Alias for backward compatibility
generate_sha256_hash = generate_file_hash
