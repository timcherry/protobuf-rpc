import zmq
from common.base_server import ProtoBufRPCServer


class ZeroMQServer(ProtoBufRPCServer):
    def __init__(self, host, port, service):
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://%s:%s" % (host, port))
        self.service = service

    def serve_forever(self,):
        while True:
            request = self.socket.recv()
            import pdb; pdb.set_trace()
            response = self.handle(request)
            self.socket.send(response.SerializeToString())
