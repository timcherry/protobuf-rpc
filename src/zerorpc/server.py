import zmq
import protos.rpc_pb2 as rpc_pb
from controller import SocketRpcController

class Callback(object):
    '''Class to allow execution of client-supplied callbacks.'''

    def __init__(self):
        self.invoked = False
        self.response = None

    def run(self, response):
        self.response = response
        self.invoked = True

class ZeroMQServer(object):
    def __init__(self, host, port, service):
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://%s:%s" % (host, port))
        self.service = service

    def serve_forever(self,):
        while True:
            request = self.socket.recv()
            response = self._handle(request)
            self.socket.send(response.SerializeToString())

    def _handle(self, request):
        req_obj = self._parse_outer_request(request)
        method = self._get_method(req_obj.method_name)
        req_proto = self._parse_inner_request(req_obj, method)
        response = self._do_request(method, req_proto)
        return response

    def _parse_outer_request(self, request):
        req_obj = rpc_pb.Request()
        req_obj.ParseFromString(request)
        return req_obj

    def _get_method(self, method_name):
        return self.service.DESCRIPTOR.FindMethodByName(method_name)

    def _parse_inner_request(self, request, method):
        proto_req = self.service.GetRequestClass(method)()
        proto_req.ParseFromString(request.request_proto)
        return proto_req

    def _do_request(self, method, proto_request):
        controller = SocketRpcController()
        callback = Callback()
        self.service.CallMethod(method, controller, proto_request, callback)
        response = rpc_pb.Response()
        response.response_proto = callback.response.SerializeToString()
        return response
