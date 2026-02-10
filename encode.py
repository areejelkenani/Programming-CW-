# Magic header to identify images encoded by this program
# this helps the decoder verify that a msg actually exists 
HEADER = "STEG"

# Binary terminator added to detect the end of the message
TERMINATOR = "1111111111111110"

# Reads the BMP image as raw bytes so we can directly access pixel data
def read_bmp_bytes(filename):
    with open(filename, "rb") as f:
        return bytearray(f.read())

# Writes modified bytes back to a new BMP file
def write_bmp_bytes(filename, data):
    with open(filename, "wb") as f:
        f.write(data)

# Converts each character of the message into 8-bit binary
def text_to_binary(message):
    binary = ""
    for char in message:
        binary += format(ord(char), "08b")
    return binary

# Replaces the LSB of a byte with the given bit (the core operation used in LSB steg)
def set_LSB(byte, bit):
    return (byte & 0b11111110) | int(bit)

# Encodes the secret message inside the BMP image
def encode_image(image_file, user_input, is_file):
    bmp_data = read_bmp_bytes(image_file)

    # Separate header and pixel data
    # the header stays unchanged to maintain image structure
    header = bmp_data[:54]
    pixel_data = bmp_data[54:]

    # Read message either from user input or from a text file
    if is_file.lower() == "y":
        with open(user_input, "r") as f:
            secret_message = f.read().strip()
    else:
        secret_message = user_input

    # Add magic header before the actual message
    full_message = HEADER + secret_message

    # Convert message to binary and add terminator
    binary_message = text_to_binary(full_message)
    binary_message += TERMINATOR

    # Check if image can store the full message
    if len(binary_message) > len(pixel_data):
        print("Message too long for this image.")
        return

    # Embed each bit into the LSB of pixel bytes
    for i in range(len(binary_message)):
        pixel_data[i] = set_LSB(pixel_data[i], binary_message[i])

    # Output filename for the encoded image
    output_file = "encoded_image.bmp"

    # Combine header and modified pixel data
    new_bmp = header + pixel_data
    write_bmp_bytes(output_file, new_bmp)

    print("Message encoded successfully.")
    print("Saved as:", output_file)
