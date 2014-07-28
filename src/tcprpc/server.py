from common.base_server import ProtoBufRPCServer
from gevent.server import StreamServer


class GeventStreamServer(ProtoBufRPCServer):
    def __init__(self, host, port, service):
        self.server = StreamServer((host, port), self.read_inbound)
        self.service = service

    def serve_forever(self,):
        self.server.serve_forever()

    def read_inbound(self, socket, address):
        import pdb; pdb.set_trace()
