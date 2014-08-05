from gevent import monkey
monkey.patch_all()

from protobuf_rpc.server import GServer
import unittest
import zmq.green as zmq
from mock import MagicMock, patch

class TestGServer(unittest.TestCase):

    @patch("protobuf_rpc.server.Pool")
    @patch("protobuf_rpc.server.Event")
    @patch("protobuf_rpc.server.Context")
    @patch("protobuf_rpc.server.zmq")
    def setUp(self, mock_pool, mock_event, mock_ctx, mock_zmq):
        zmq.Context.return_value = "FOFOF"
        self.mock_context = mock_ctx
        self.mock_service = MagicMock()

    def test_router_socket_type(self):

        with patch
        self.server = GServer("127.0.0.1",
                              1234,
                              self.mock_service)

        #self.mock_context.socket.assert_called_with(zmq.ROUTER)

    def test_bind(self):
        pass

