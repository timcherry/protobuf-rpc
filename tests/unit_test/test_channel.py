from gevent import monkey
monkey.patch_all()

import gevent
from protobuf_rpc.channel import ZMQChannel
from protobuf_rpc.controller import SocketRpcController
from protobuf_rpc.server import GServer
from TestService_pb2 import Request, Response, TestService_Stub, TestService
import unittest

class TestServer(TestService):
    def Query(self, controller, request, done):
        assert  request.query == "PING"
        response = Response()
        response.response = "PONG"
        done.run(response)


class TestChannel(unittest.TestCase):
    def setUp(self,):
        self.hosts = [("127.0.0.1",12345)]
        self.channel = ZMQChannel(hosts=self.hosts, pool_size=1, max_pool_size=1)
        self.service = TestService_Stub(self.channel)
        self.controller = SocketRpcController()
        self.server = GServer("127.0.0.1", 12345, TestServer(), poolsize=1)
        self.server_thread = gevent.spawn(self.server.serve_forever)


    def tearDown(self,):
        self.server.shutdown()
        self.server_thread.join()


    def test_send_rpc(self):
        req = Request()
        req.query = "PING"
        resp = TestService_Stub.Query(self.service,
                               self.controller,
                               req)
        self.assertEquals(resp.response, "PONG")
