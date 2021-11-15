import zmq

context = zmq.Context()
socket = context.socket(zmq.XSUB)
socket.connect("tcp://localhost:5560")

# socket.send(b'\x01Hello')
socket.send_multipart([b'\x01Hello', b'ID do crls'])
socket.send(b'\x01World')
socket.send(b'\x02Hello')

# socket.setsockopt_string(zmq.SUBSCRIBE, "Hello")

while True:
    message = socket.recv()
    print(f"Received request: {message}")
