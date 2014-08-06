from gevent import monkey
monkey.patch_all()

from gevent.pool import Pool
from gevent.event import Event
import zmq.green as zmq
from protobuf_rpc.base_server import ProtoBufRPCServer


class GServer(ProtoBufRPCServer):
    def __init__(self, host, port, service, poolsize=128):
        self.gpool = Pool(poolsize)
        self.stop_event = Event()
        context = zmq.Context()
        self.port = port
        self.socket = context.socket(zmq.ROUTER)
        self.socket.bind("tcp://%s:%s" % (host, port))
        self.service = service

    def serve_forever(self,):
        while not self.stop_event.is_set():
            msg = self.socket.recv_multipart()
            self.gpool.spawn(self.handle_request, msg)

    def shutdown(self,):
        self.stop_event.set()

    def handle_request(self, msg):
        assert len(msg) == 3
        (id_, null, request) = msg
        assert null == ''
        response = self.handle(request)
        self.socket.send_multipart([id_, null, response.SerializeToString()])

