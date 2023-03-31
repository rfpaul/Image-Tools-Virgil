import os
import random

def read_image_file(filepath):
    with open(filepath, "rb") as f:
        return bytearray(f.read())

def write_image_file(filepath, data):
    with open(filepath, "wb") as f:
        f.write(data)

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

def undo_databend(image_data, changes):
    for index, old_value in reversed(changes):
        image_data[index] = old_value
    return image_data

def main():
    filepath = "/path/to/your/image/file"
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
    main()
