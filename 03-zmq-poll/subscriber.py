#
#   Based on zguide examples
#   Weather update client
#   Connects SUB socket to tcp://localhost:5556
#   Collects weather updates and finds avg temp in zipcode
#

import sys
import zmq


#  Socket to talk to server
context = zmq.Context()
us_socket = context.socket(zmq.SUB)
pt_socket = context.socket(zmq.SUB)

print("Collecting updates from american weather server...")
us_socket.connect("tcp://localhost:5556")
print("Collecting updates from portuguese weather server...")
pt_socket.connect("tcp://localhost:5557")

# Subscribe to zipcode, default is NYC, 10001
zip_filter = sys.argv[1] if len(sys.argv) > 1 else "4575"
us_socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)
pt_socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)

poller = zmq.Poller()
poller.register(us_socket, zmq.POLLIN)
poller.register(pt_socket, zmq.POLLIN)

while True:
    try:
        socks = dict(poller.poll())
    except KeyboardInterrupt:
        break

    if us_socket in socks:
        message = us_socket.recv()
        print("Received from US")
        print(message)
        break

    if pt_socket in socks:
        message = pt_socket.recv()
        print("Received from PT")
        print(message)
        break