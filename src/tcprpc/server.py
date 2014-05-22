import socket
from common.base_server import ProtoBufRPCServer


class RawTCPServer(ProtoBufRPCServer):
    def __init__(self, host, port, service):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.service = service

    def serve_forever(self,):
        self.socket.listen(5)
        while True:
            conn, addr = self.socket.accept()
            byte_stream = conn.recv(1024)
            response = self.handle(byte_stream)
            conn.send(response.SerializeToString())
