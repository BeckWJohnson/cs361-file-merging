import zmq
import time

context = zmq.Context()

print("Connecting to merge microservice")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5556")

print("\n--- Test 1: Valid merge ---")
socket.send(b"merge!fileA.txt!fileB.txt!merged_output.txt")
message = socket.recv()
print("Expected: Success")
print("Received:", message)
print()

time.sleep(1)

print("\n--- Test 2: Invalid filename ---")
socket.send(b"merge!bad file.!fileB.txt!merged.txt")  # fails regex
message = socket.recv()
print("Expected: filename error")
print("Received:", message)
print()

time.sleep(1)

print("\n--- Test 3: Unsupported operation ---")
socket.send(b"append!fileA.txt!fileB.txt!out.txt")
message = socket.recv()
print("Expected: error message")
print("Received:", message)
print()

time.sleep(1)
