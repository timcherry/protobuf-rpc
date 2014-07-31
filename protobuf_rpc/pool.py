import zmq.green as zmq
from Queue import Queue

class ObjectPool(object):
    def __init__(self, obj=None, size=None, maxsize=None, *args, **kwargs):
        self.queue = Queue(maxsize = maxsize)
        self.maxsize = maxsize
        self.size = size
        self.obj = obj
        self.args = args
        self.kwargs = kwargs
        [self.queue.put(obj(*self.args, **self.kwargs)) for i in range(size)]

    def get(self, block=True, timeout=None):
        if self.queue.empty():
            self.queue.put(self.obj(*self.args, **self.kwargs))
        return self.queue.get()

    def release(self, obj):
        assert isinstance(obj, self.obj)
        self.queue.put(obj)


class ZMQConnection(object):
    def __init__(self, hosts):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        [
            self.socket.connect("tcp://%s:%s" % (host, port))
            for (host, port) in hosts
        ]

    def send(self, req):
        self.socket.send(req)

    def recv(self,):
        resp = self.socket.recv()
        return resp
