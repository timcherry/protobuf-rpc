import zmq.green as zmq
import random


class ZMQConnection(object):

    def __init__(self, hosts):
        context = zmq.Context()
        random.shuffle(hosts)
        self.socket = context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.LINGER, 0)
        [
            self.socket.connect("tcp://%s:%s" % (host, port))
            for (host, port) in hosts
        ]
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)

    def send(self, req):
        self.socket.send(req)

    def recv(self, timeout=2*1000):
        if self.poller.poll(timeout):
            resp = self.socket.recv()
        else:
            # TODO: remove host that just timedout
            raise IOError("Timeout processing request.")
        return resp