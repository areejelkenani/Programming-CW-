# magic header used to verify that the image was encoded by this program
HEADER = "STEG"
# terminator used to detect the end of the hidden msg
TERMINATOR = "1111111111111110"

# reads the BMP file as raw bytes
def read_bmp_bytes(filename):
    with open(filename, "rb") as f:
        return bytearray(f.read())

# extracts the LSB from a byte
def get_LSB(byte):
    return format(byte, "08b")[-1]

# converts a binary string back into readable text
def binary_to_text(binary_message):
    text = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if len(byte) == 8:
            text += chr(int(byte, 2))
    return text

# decodes a hidden msg from an encoded BMP image 
def decode_image(encoded_file):
    # read image bytes and skip the BMP header 
    bmp_data = read_bmp_bytes(encoded_file)
    pixel_data = bmp_data[54:]

    binary_message = ""

    #extracts LSBs from pixel data
    for byte in pixel_data:
        binary_message += get_LSB(byte)
        # stop reading pnce the terminator is detected 
        if binary_message.endswith(TERMINATOR):
            binary_message = binary_message[:-len(TERMINATOR)]
            break
    else:
        # if no terminator is found, the image is not steg
        print("No hidden message detected.")
        return
    # convert extracted binary data into text
    decoded_text = binary_to_text(binary_message)

    # verify the persence of magic header to prevent decoding random images
    if not decoded_text.startswith(HEADER):
        print("No hidden message detected.")
        return
    #remove the header and display the actual secret msg
    secret_message = decoded_text[len(HEADER):]

    print("Decoded message:")
    print(secret_message)
