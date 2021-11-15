import zmq
import time

#  Prepare our context and sockets
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect("tcp://localhost:5559")

time.sleep(1) # next time synchronize them with a req rep but now im lazy

#  Do 10 requests, waiting each time for a response
for request in range(1, 11):
    socket.send_string("Hello World")
    print(f"SENT")
