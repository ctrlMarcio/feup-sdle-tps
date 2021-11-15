# Simple xpub-xsub broker
#
# Inspired by Lev Givon <lev(at)columbia(dot)edu>

import zmq
from zmq.utils.monitor import recv_monitor_message
import threading

# Prepare our context and sockets
context = zmq.Context()
pub_end = context.socket(zmq.XSUB)
sub_end = context.socket(zmq.XPUB)
pub_end.bind("tcp://*:5559")
sub_end.bind("tcp://*:5560")

# Start the monitor thread
EVENT_MAP = {}
print("Event names:")
for name in dir(zmq):
    if name.startswith('EVENT_'):
        value = getattr(zmq, name)
        print("%21s : %4i" % (name, value))
        EVENT_MAP[value] = name


monitor = sub_end.get_monitor_socket()
def event_monitor(monitor):
    while monitor.poll():
        evt = recv_monitor_message(monitor)
        evt.update({'description': EVENT_MAP[evt['event']]})
        print("Event: {}".format(evt))
        if evt['event'] == zmq.EVENT_MONITOR_STOPPED:
            break
    monitor.close()
    print()
    print("event monitor thread done!")


monitor_thread = threading.Thread(target=event_monitor, args=(monitor,))
monitor_thread.start()

pub_end.send(b'\x01')

# Initialize poll set
poller = zmq.Poller()
poller.register(pub_end, zmq.POLLIN)
poller.register(sub_end, zmq.POLLIN)

# Switch messages between sockets
while True:
    socks = dict(poller.poll())

    if socks.get(pub_end) == zmq.POLLIN:
        msg = pub_end.recv()
        print(msg)
        sub_end.send(msg)

    if socks.get(sub_end) == zmq.POLLIN:
        msg = sub_end.recv_multipart()
        print(msg)
