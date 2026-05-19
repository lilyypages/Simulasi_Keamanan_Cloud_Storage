from PIL import Image
import json


END_MARKER = "#####END#####"


# Convert text to binary
def text_to_binary(text):

    binary = ''.join(
        format(ord(char), '08b')
        for char in text
    )

    return binary


# Convert binary to text
def binary_to_text(binary):

    chars = []

    for i in range(0, len(binary), 8):

        byte = binary[i:i+8]

        chars.append(chr(int(byte, 2)))

    return ''.join(chars)


# Embed metadata into image
def embed_metadata(image_path, metadata, output_path):

    # Open image
    image = Image.open(image_path)

    encoded = image.copy()

    # Convert metadata dict to JSON string
    metadata_json = json.dumps(metadata)

    # Add end marker
    secret_data = metadata_json + END_MARKER

    # Convert to binary
    binary_data = text_to_binary(secret_data)

    data_index = 0

    pixels = encoded.load()

    width, height = encoded.size

    for y in range(height):

        for x in range(width):

            pixel = list(pixels[x, y])

            for n in range(3):

                if data_index < len(binary_data):

                    # Replace LSB
                    pixel[n] = (
                        pixel[n] & ~1
                    ) | int(binary_data[data_index])

                    data_index += 1

            pixels[x, y] = tuple(pixel)

            if data_index >= len(binary_data):
                break

        if data_index >= len(binary_data):
            break

    encoded.save(output_path)

    print("[+] Metadata embedded into image")


# Extract metadata from image
def extract_metadata(image_path):

    image = Image.open(image_path)

    binary_data = ""

    pixels = image.load()

    width, height = image.size

    for y in range(height):

        for x in range(width):

            pixel = pixels[x, y]

            for n in range(3):

                binary_data += str(pixel[n] & 1)

    # Convert binary to text
    extracted_text = binary_to_text(binary_data)

    # Find end marker
    end_index = extracted_text.find(END_MARKER)

    if end_index == -1:
        return None

    metadata_json = extracted_text[:end_index]

    metadata = json.loads(metadata_json)

    return metadata