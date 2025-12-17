#binary terminator added to mark the end of the msg
TERMINATOR = "00000000"

#reads the BMP image as raw bytes
def read_bmp_bytes(filename):
    with open(filename, "rb") as f:
        return bytearray(f.read())

#writes modified byytes back to a new BMP file 
def write_bmp_bytes(filename, data):
    with open(filename, "wb") as f:
        f.write(data)

#converts each character of the msg into 8-bit binary 
def text_to_binary(message):
    binary = ""
    for char in message:
        binary += format(ord(char), "08b")
    return binary

#replaces the LSB of a byte with the given bit 
def set_LSB(byte, bit):
    return (byte & 0b11111110) | int(bit)

#encodes the secret msg inside the BMP image 
def encode_image(image_file, user_input, is_file):
    bmp_data = read_bmp_bytes(image_file)

    #separate header and pixel data
    header = bmp_data[:54]
    pixel_data = bmp_data[54:]

    #read msg either from user input or from a text file 
    if is_file.lower() == "y":
        with open(user_input, "r") as f:
            secret_message = f.read().strip()
    else:
        secret_message = user_input

    #convert msg to binary and add terminator 
    binary_message = text_to_binary(secret_message)
    binary_message += TERMINATOR

    #check if image can store the full msg 
    if len(binary_message) > len(pixel_data):
        print("Message too long for this image.")
        return
    
    #include each bit into the LSB of pixel bytes 
    for i in range(len(binary_message)):
        pixel_data[i] = set_LSB(pixel_data[i], binary_message[i])

    # auto output filename
    output_file = "encoded_image.bmp"

    #combine header and modified pixel data 
    new_bmp = header + pixel_data
    write_bmp_bytes(output_file, new_bmp)

    print("Message encoded successfully.")
    print("Saved as:", output_file)