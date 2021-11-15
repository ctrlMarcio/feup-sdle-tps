#
#   Request-reply service in Python
#   Connects REP socket to tcp://localhost:5560
#   Expects "Hello" from client, replies with "World"
#
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5560")

socket.setsockopt_string(zmq.SUBSCRIBE, "Hello")

while True:
    message = socket.recv()
    print(f"Received request: {message}")
