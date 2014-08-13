from gevent import monkey
monkey.patch_all()

import gevent
from protobuf_rpc.channel import ZMQChannel
from protobuf_rpc.controller import SocketRpcController
from protobuf_rpc.server import GServer
from protobuf_rpc.error import *
from TestService_pb2 import Request, Response, TestService_Stub, TestService
import unittest

class TestServer(TestService):
    def Query(self, controller, request, done):
        assert request.query == "PING"
        response = Response()
        response.response = "PONG"
        done.run(response)


class TestErrorServer(TestService):
    def BadQuery(self, controller, request, done):
        assert False

class TestChannel(unittest.TestCase):
    def setUp(self,):
        self.hosts = [("127.0.0.1",12345)]
        self.channel = ZMQChannel(hosts=self.hosts, pool_size=1, max_pool_size=1)
        self.service = TestService_Stub(self.channel)
        self.controller = SocketRpcController()

        self.server = GServer("127.0.0.1", 12345, TestServer(), poolsize=1)
        self.server_thread = gevent.spawn(self.server.serve_forever)

        self.bad_hosts = [("127.0.0.1",12346)]
        self.bad_channel = ZMQChannel(hosts=self.bad_hosts, pool_size=1, max_pool_size=1)
        self.bad_service = TestService_Stub(self.bad_channel)
        self.bad_controller = SocketRpcController()
        self.bad_server = GServer("127.0.0.1", 12346, TestErrorServer(), poolsize=1)
        self.bad_server_thread = gevent.spawn(self.bad_server.serve_forever)

    def tearDown(self,):
        self.server.shutdown()
        self.server_thread.join()
        self.bad_server.shutdown()
        self.bad_server_thread.join()

    def test_send_rpc(self):
        req = Request()
        req.query = "PING"
        resp = self.service.Query(self.controller,
                                  req)
        self.assertEquals(resp.response, "PONG")

    def test_not_implemented(self):
        req = Request()
        req.query = "PING"
        self.assertRaises(MethodNotFoundError,
                          self.service.BadQuery,
                          self.controller,
                          req)

    def test_server_error(self,):
        req = Request()
        req.query = "PING"
        self.assertRaises(RpcError,
                          self.bad_service.BadQuery,
                          self.bad_controller,
                          req)

