from protobuf_rpc.common.base_server import ProtoBufRPCServer
from gevent.server import StreamServer


class GeventStreamServer(ProtoBufRPCServer):
    def __init__(self, host, port, service):
        self.server = StreamServer((host, port), self.__handle)
        self.service = service

    def serve_forever(self,):
        self.server.serve_forever()

    def __handle(self, socket, address):
        request = socket.recv(1024)
        response = self.handle(request)
        socket.send(response.SerializeToString())
