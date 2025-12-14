TERMINATOR = "00000000"


def read_bmp_bytes(filename):
    with open(filename, "rb") as f:
        return bytearray(f.read())


def write_bmp_bytes(filename, data):
    with open(filename, "wb") as f:
        f.write(data)

def text_to_binary(message):
    binary = ""
    for char in message:
        binary += format(ord(char), "08b")
    return binary


def set_LSB(byte, bit):
    return (byte & 0b11111110) | int(bit)


def encode_image(image_file, user_input, is_file):
    bmp_data = read_bmp_bytes(image_file)

    header = bmp_data[:54]
    pixel_data = bmp_data[54:]

    if is_file.lower() == "y":
        with open(user_input, "r") as f:
            secret_message = f.read().strip()
    else:
        secret_message = user_input

    binary_message = text_to_binary(secret_message)
    binary_message += TERMINATOR

    if len(binary_message) > len(pixel_data):
        print("Message too long for this image.")
        return

    for i in range(len(binary_message)):
        pixel_data[i] = set_LSB(pixel_data[i], binary_message[i])

    # auto output filename
    output_file = "encoded_image.bmp"

    new_bmp = header + pixel_data
    write_bmp_bytes(output_file, new_bmp)

    print("Message encoded successfully.")
    print("Saved as:", output_file)