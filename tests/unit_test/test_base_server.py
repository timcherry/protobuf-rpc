import unittest
from protobuf_rpc.protos.rpc_pb2 import Request, Response, RPC_ERROR, \
    INVALID_REQUEST_PROTO, METHOD_NOT_FOUND, BAD_REQUEST_PROTO
from protobuf_rpc.base_server import ProtoBufRPCServer
from TestService_pb2 import TestService
from TestService_pb2 import Request as TestRequest
from TestService_pb2 import Response as TestResponse

class TestServer(TestService):
    def Query(self, controller, request, done):
        assert request.query == "PING"
        response = TestResponse()
        response.response = "PONG"
        done.run(response)

class TestProtoBufRPCServer(unittest.TestCase):

    def setUp(self):
        self.pb_server = ProtoBufRPCServer()
        self.pb_server.service = TestServer()

    def test_bad_outer(self):
        bad_request = "abc"
        response = self.pb_server.handle(bad_request)
        self.assertEquals(response.error_code, INVALID_REQUEST_PROTO)

    def test_bad_method(self,):
        bad_request = Request()
        bad_request.method_name = "NotQuery"
        bad_request.service_name = "TestService"
        bad_request.request_proto =  "Foobar"
        response = self.pb_server.handle(bad_request.SerializeToString())
        self.assertEquals(response.error_code, METHOD_NOT_FOUND)

    def test_bad_request_proto(self):
        bad_request = Request()
        bad_request.method_name = "Query"
        bad_request.service_name = "TestService"
        bad_request.request_proto =  "Foobar"
        response = self.pb_server.handle(bad_request.SerializeToString())
        self.assertEquals(response.error_code, BAD_REQUEST_PROTO)


    def test_bad_request_proto(self):
        bad_request = Request()
        bad_request.method_name = "Query"
        bad_request.service_name = "TestService"
        test_request = TestRequest()
        test_request.query = "NOTPING"
        bad_request.request_proto = test_request.SerializeToString()
        response = self.pb_server.handle(bad_request.SerializeToString())
        self.assertEquals(response.error_code, RPC_ERROR)

