import re
import zmq
import os

context = zmq.Context()
PORT = 5556                  # New port so it doesn't collide with your old server
SEPARATOR = b'\x21'          # '!' ASCII

# File name validation regex (same as original)
PATTERN = re.compile(r"^[\w\-()\[\]\.\ ]*[\w\-()\[\]]$")


def validate_filename(name, pattern, socket):
    """Validate filename and send error messages the same way the original server does."""
    if not pattern.match(name):
        socket.send(b"ERROR: Invalid filename")
        return False
    return True


def merge_files(file1, file2, new_file):
    """Perform the actual merge."""
    try:
        with open("files/" + file1, "r") as f1:
            data1 = f1.read()
        with open("files/" + file2, "r") as f2:
            data2 = f2.read()

        with open("files/" + new_file, "w") as out:
            out.write(data1)
            out.write(data2)

        return True, b"Success: Files merged"
    except Exception as e:
        return False, f"ERROR: {e}".encode()


def process_operation(operation, file1, file2, new_file):
    if operation != "merge":
        return False, b"ERROR: Unsupported operation"

    return merge_files(file1, file2, new_file)


def main():
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{PORT}")
    print(f"Merge microservice running on port {PORT}")

    while True:
        buffer = socket.recv()

        # Expect format:  operation!file1!file2!new_file
        parts = buffer.decode().split("!")

        if len(parts) != 4:
            socket.send(b"ERROR: Bad request format")
            continue

        operation, file1, file2, new_file = parts
        print(f"Operation: {operation}")
        print(f"File1: {file1}")
        print(f"File2: {file2}")
        print(f"New file: {new_file}")

        # Validate file names
        if not validate_filename(file1, PATTERN, socket): continue
        if not validate_filename(file2, PATTERN, socket): continue
        if not validate_filename(new_file, PATTERN, socket): continue

        # Process
        ok, response = process_operation(operation, file1, file2, new_file)

        # Send reply
        socket.send(response)
        print()


if __name__ == "__main__":
    main()
