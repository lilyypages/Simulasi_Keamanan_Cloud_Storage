import logging
import json
from PIL import Image

logger = logging.getLogger(__name__)

END_MARKER = "#####END#####"


def text_to_binary(text):
    """Convert text to binary string."""
    return ''.join(format(ord(char), '08b') for char in text)


def binary_to_text(binary):
    """Convert binary string to text."""
    return ''.join(
        chr(int(binary[i:i+8], 2))
        for i in range(0, len(binary), 8)
    )


def embed_metadata(image_path, metadata, output_path):
    """Embed metadata into image using LSB steganography."""
    image = Image.open(image_path)
    encoded = image.copy()

    metadata_json = json.dumps(metadata)
    secret_data = metadata_json + END_MARKER
    binary_data = text_to_binary(secret_data)

    # Validate capacity
    width, height = encoded.size
    max_capacity = width * height * 3  # 3 channels per pixel
    if len(binary_data) > max_capacity:
        raise ValueError(
            f"Metadata terlalu besar ({len(binary_data)} bits) "
            f"untuk gambar ini (kapasitas: {max_capacity} bits)"
        )

    data_index = 0
    pixels = encoded.load()

    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x, y])
            for n in range(3):
                if data_index < len(binary_data):
                    pixel[n] = (pixel[n] & ~1) | int(binary_data[data_index])
                    data_index += 1
            pixels[x, y] = tuple(pixel)
            if data_index >= len(binary_data):
                break
        if data_index >= len(binary_data):
            break

    encoded.save(output_path)
    logger.info(f"Metadata embedded into image: {output_path}")
    return output_path


def extract_metadata(image_path):
    """Extract metadata from image with early termination."""
    image = Image.open(image_path)
    pixels = image.load()
    width, height = image.size

    binary_data = ""
    extracted_text = ""

    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            for n in range(3):
                binary_data += str(pixel[n] & 1)

                # Every 8 bits, convert to character and check end marker
                if len(binary_data) == 8:
                    extracted_text += chr(int(binary_data, 2))
                    binary_data = ""

                    if extracted_text.endswith(END_MARKER):
                        metadata_json = extracted_text[:-len(END_MARKER)]
                        return json.loads(metadata_json)

    return None
