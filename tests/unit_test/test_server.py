from gevent import monkey
monkey.patch_all()

from protobuf_rpc.server import GServer
import unittest
from mock import MagicMock, patch
import socket
from TestService_pb2 import Request, Response, TestService_Stub, TestService

class TestServer(TestService):
    def Query(self, controller, request, done):
        assert request.query == "PING"
        response = Response()
        response.response = "PONG"
        done.run(response)

class TestGServer(unittest.TestCase):

    @patch("protobuf_rpc.server.Pool")
    @patch("protobuf_rpc.server.Event")
    def setUp(self, mock_pool, mock_event):
        self.mock_service = MagicMock()
        self.port = 6969
        self.host = "127.0.0.1"
        self.server = GServer(self.host,
                              self.port,
                              self.mock_service)

    def test_socket_listening(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((self.host, self.port))
        self.assertEquals(result, 0)




