from gevent import monkey
monkey.patch_all()

from gevent.pool import Pool
from gevent.event import Event
from protobuf_rpc.base_server import ProtoBufRPCServer
import zmq


class GServer(ProtoBufRPCServer):
    def __init__(self, host, port, service):
        self.gpool = Pool(1024)
        self.stop_event = Event()
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://%s:%s" % (host, port))
        self.service = service

    def serve_forever(self,):
        while not self.stop_event.is_set():
            request = self.socket.recv()
            self.handle_request(request)
            #self.gpool.spawn(self.handle_request, request)

    def shutdown(self,):
        self.stop_event.set()

    def handle_request(self, request):
        response = self.handle(request)
        self.socket.send(response.SerializeToString())

