#terminator usued to detect the end of the hidden msg
TERMINATOR = "00000000"  

#reads the BMP file as raw bytes so we can access pixel data
def read_bmp_bytes(filename):                           
    with open(filename, "rb") as f:
        return bytearray(f.read())

#returns the LSB of a byte
def get_LSB(byte):                                     
    return format(byte, "08b")[-1]

#converts a binary string back into readable text
def binary_to_text(binary_message):
    text = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        if len(byte) == 8:
            value = int(byte, 2)
            #stop decoding when terminator is reached 
            if value == 0:
                break
            text += chr(value)
    return text

#extracts the hidden msg from the encoded BMP image 
def decode_image(encoded_file):
    #read all bytes from the encoded image 
    bmp_data = read_bmp_bytes(encoded_file)
    #skip BMP header (first 54 bytes)
    pixel_data = bmp_data[54:]

    binary_message = ""

    #read LSB from pixel data until terminator is found 
    for byte in pixel_data:
        binary_message += get_LSB(byte)
        #check for terminator every 8 bits
        if len(binary_message) % 8 == 0:
            if binary_message[-8:] == TERMINATOR:
                break

    #convert extracted binary data back to text 
    secret_message = binary_to_text(binary_message)

    print("Decoded message:")
    print(secret_message)