import zmq
from common.base_channel import ProtoBufRPCChannel


class ZeroMQChannel(ProtoBufRPCChannel):
    def __init__(self, host='localhost', port=8090):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://%s:%s" % (host, port))

    def send_rpc_request(self, rpcRequest):
        self.socket.send(rpcRequest.SerializeToString())

    def recv_response(self):
        resp = self.socket.recv()
        return resp

