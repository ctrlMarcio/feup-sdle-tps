# Simple xpub-xsub broker
#
# Inspired by Lev Givon <lev(at)columbia(dot)edu>

import zmq
import threading

# Prepare our context and sockets
context = zmq.Context()
pub_end = context.socket(zmq.XSUB)
sub_end = context.socket(zmq.XPUB)
pub_end.bind("tcp://*:5559")
sub_end.bind("tcp://*:5560")

# Start the loggin thread
def log():
    receiver = context.socket(zmq.PAIR)
    receiver.bind("inproc://log")

    # Socket to talk to logging server
    while True:
        msg = receiver.recv()
        print(msg)

thread = threading.Thread(target=log)
thread.start()

cap = context.socket(zmq.PAIR)
cap.connect("inproc://log")

zmq.proxy(pub_end, sub_end, capture=cap)