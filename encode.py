TERMINATOR = "00000000"


def read_bmp_bytes(filename):
    with open(filename, "rb") as f:
        return bytearray(f.read())


def get_LSB(byte):
    return format(byte, "08b")[-1]


def binary_to_text(binary_message):
    text = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        if len(byte) == 8:
            value = int(byte, 2)
            if value == 0:
                break
            text += chr(value)
    return text


def decode_image(encoded_file):
    bmp_data = read_bmp_bytes(encoded_file)
    pixel_data = bmp_data[54:]

    binary_message = ""

    for byte in pixel_data:
        binary_message += get_LSB(byte)
        if len(binary_message) % 8 == 0:
            if binary_message[-8:] == TERMINATOR:
                break

    secret_message = binary_to_text(binary_message)

    print("Decoded message:")
    print(secret_message)