"""
Databending Script for JPEG, JP2, and HEIC files

This script allows you to apply databending to various image file formats,
including JPEG, JP2, and HEIC. It modifies the image file in-place and provides
options to flip random bytes, undo changes, and save the modified image to a
new file. Please note that you may need to adjust the start and end values in
the databend function to avoid corrupting the file header for different file
types.

GPL 3.0, (c) 2023 Robert Paul
Special thanks to @letsglitchit AKA Dawnia Darkstone for inspiring me to
explore glitch art and for sharing the love, practice, and techniques of glitch
art with the creative community.

Large portions generated with GPT-4
"""
"""
Databending Script for JPEG, JP2, and HEIC files

This script allows you to apply databending to various image file formats,
including JPEG, JP2, and HEIC. It modifies the image file in-place and provides
options to flip random bytes, undo changes, and save the modified image to a
new file. Please note that you may need to adjust the start and end values in
the databend function to avoid corrupting the file header for different file
types.
"""

import os
import random
import argparse

# Function to read image data from a file
def read_image_file(filepath):
    with open(filepath, "rb") as f:
        return bytearray(f.read())

# Function to write image data to a file
def write_image_file(filepath, data):
    with open(filepath, "wb") as f:
        f.write(data)

# Function to apply databending to the image data
def databend(image_data, databend_steps=1):
    changes = []

    # Define the start and end points of the image-encoding region
    # You may need to adjust these values based on the file format
    start = 1000
    end = len(image_data) - 1000

    for _ in range(databend_steps):
        index = random.randint(start, end)
        old_value = image_data[index]
        new_value = random.choice([0x00, 0xFF])
        image_data[index] = new_value
        changes.append((index, old_value))

    return image_data, changes

# Function to revert the databending changes
def undo_databend(image_data, changes):
    for index, old_value in reversed(changes):
        image_data[index] = old_value
    return image_data

# Main function that handles user input and file operations
def main(filepath):
    if not os.path.exists(filepath):
        print("File not found")
        return

    _, file_extension = os.path.splitext(filepath)
    supported_extensions = ['.jpg', '.jpeg', '.jp2', '.heic']

    if file_extension.lower() not in supported_extensions:
        print("Unsupported file type")
        return

    image_data = read_image_file(filepath)
    undo_stack = []

    while True:
        action = input("Enter action (f=flip, u=undo, s=save, q=quit): ").lower()

        if action == "f":
            image_data, changes = databend(image_data)
            undo_stack.append(changes)
            write_image_file(filepath, image_data)
            print("Databending applied. Open the image to see the changes.")
        elif action == "u":
            if not undo_stack:
                print("No actions to undo.")
            else:
                changes = undo_stack.pop()
                image_data = undo_databend(image_data, changes)
                write_image_file(filepath, image_data)
                print("Undo applied. Open the image to see the changes.")
        elif action == "s":
            save_path = input("Enter the save path: ")
            write_image_file(save_path, image_data)
            print(f"Image saved as {save_path}")
        elif action == "q":
            break
        else:
            print("Invalid action")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", nargs="?", default="/image/filepath/here.heic", help="Path to the image file")
    args = parser.parse_args()

    main(args.filepath)
