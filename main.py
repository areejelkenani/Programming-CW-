from encode import encode_image
from decode import decode_image


def main():
    while True:
        print("\n---- STEGANOGRAPHY PROGRAM ----")
        print("1. Encode a message")
        print("2. Decode a message")
        print("3. Exit")

        choice = input("Choose 1, 2, or 3: ")

        if choice == "1":
            image_file = input("Enter image BMP filename: ")
            is_file = input("Is your message inside a file? (y/n): ")
            user_input = input("Enter the message OR file name: ")

            encode_image(image_file, user_input, is_file)

        elif choice == "2":
            encoded_file = input("Enter encoded BMP filename: ")
            decode_image(encoded_file)

        elif choice == "3":
            print("Goodbye.")
            break

        else:
            print("Invalid option.")


main()