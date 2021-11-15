import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
  message = socket.recv()
  print(f"Received request: {message.decode('utf-8')}")

  socket.send_string("World")
