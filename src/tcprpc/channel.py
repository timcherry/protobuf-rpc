import socket
from common.base_channel import ProtoBufRPCChannel

class RawTCPChannel(ProtoBufRPCChannel):
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def send_rpc_request(self, rpcRequest):
        self.socket.send(rpcRequest.SerializeToString())

    def recv_response(self):
        rfile = self.socket.makefile('r')
        byte_stream = rfile.read()
        return byte_stream
