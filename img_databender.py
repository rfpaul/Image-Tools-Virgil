import os
import random

def read_heic_file(filepath):
    with open(filepath, "rb") as f:
        return bytearray(f.read())

def write_heic_file(filepath, data):
    with open(filepath, "wb") as f:
        f.write(data)

def databend(heic_data, databend_steps=1):
    changes = []

    # Define the start and end points of the image-encoding region
    start = 1000
    end = len(heic_data) - 1000

    for _ in range(databend_steps):
        index = random.randint(start, end)
        old_value = heic_data[index]
        new_value = random.choice([0x00, 0xFF])
        heic_data[index] = new_value
        changes.append((index, old_value))

    return heic_data, changes

def undo_databend(heic_data, changes):
    for index, old_value in reversed(changes):
        heic_data[index] = old_value
    return heic_data

def main():
    filepath = "/filepath/goes/here.heic"
    if not os.path.exists(filepath):
        print("File not found")
        return

    heic_data = read_heic_file(filepath)
    undo_stack = []

    while True:
        action = input("Enter action (f=flip, u=undo, s=save, q=quit): ").lower()

        if action == "f":
            heic_data, changes = databend(heic_data)
            undo_stack.append(changes)
            write_heic_file(filepath, heic_data)
            print("Databending applied. Open the image to see the changes.")
        elif action == "u":
            if not undo_stack:
                print("No actions to undo.")
            else:
                changes = undo_stack.pop()
                heic_data = undo_databend(heic_data, changes)
                write_heic_file(filepath, heic_data)
                print("Undo applied. Open the image to see the changes.")
        elif action == "s":
            save_path = input("Enter the save path: ")
            write_heic_file(save_path, heic_data)
            print(f"Image saved as {save_path}")
        elif action == "q":
            break
        else:
            print("Invalid action")

if __name__ == "__main__":
    main()
