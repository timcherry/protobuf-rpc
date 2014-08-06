from protobuf_rpc.rpc_pb2 import Request, Response
from protobuf_rpc.controller import SocketRpcController
from protobuf_rpc.util import serialize_string

class Callback(object):
    '''Class to allow execution of client-supplied callbacks.'''

    def __init__(self):
        self.invoked = False
        self.response = None

    def run(self, response):
        self.response = response
        self.invoked = True


class ProtoBufRPCServer(object):
    def handle(self, request):
        req_obj = self.parse_outer_request(request)
        method = self.get_method(req_obj.method_name)
        req_proto = self.parse_inner_request(req_obj, method)
        response = self.do_request(method, req_proto)
        return response

    def parse_outer_request(self, request):
        req_obj = Request()
        req_obj.ParseFromString(request)
        return req_obj

    def get_method(self, method_name):
        return self.service.DESCRIPTOR.FindMethodByName(method_name)

    def parse_inner_request(self, request, method):
        return serialize_string(request.request_proto,
                                self.service.GetRequestClass(method))


    def do_request(self, method, proto_request):
        controller = SocketRpcController()
        callback = Callback()
        self.service.CallMethod(method, controller, proto_request, callback)
        response = Response()
        response.response_proto = callback.response.SerializeToString()
        return response

    def _serialize_response(self, conn, future):
        try:
            v = future.get(0)
        except TimeoutError:
            v = rpc_pb.Response()
            v.error_reason = v.TIMEOUT
        except:
            v.error_reason = v.ERROR

        conn.send(v.SerializeToString())

