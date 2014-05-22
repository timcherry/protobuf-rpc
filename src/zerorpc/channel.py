import zmq
from common.base_channel import ProtoBufRPCChannel


class ZeroMQChannel(ProtoBufRPCChannel):
    def __init__(self, host='localhost', port=8090):
        self.host = host
        self.port = port
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://%s:%s" % (host, port))

    def _send_rpc_request(self, rpcRequest):
        self.socket.send(rpcRequest.SerializeToString())
