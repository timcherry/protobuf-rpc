import google.protobuf.service as service
import protos.rpc_pb2 as rpc_pb
import zmq
from controller import SocketRpcController


class ZeroMQChannel(service.RpcChannel):
    def __init__(self, host='localhost', port=8090):
        self.host = host
        self.port = port
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://%s:%s" % (host, port))

    def CallMethod(self, method, controller, request, response_class, done):
        self._validate_requst(controller, request)
        rpc_request = self._create_rpc_request(method, request)
        self._send_rpc_request(rpc_request)
        response = self._recv_response()
        resp_obj = self._serialize_string(response, rpc_pb.Response)
        serialized_resp_obj = self._serialize_string(resp_obj.response_proto,
                                                     response_class)
        if done:
            done(serialized_resp_obj)

    def _validate_requst(self, controller, request):
        if controller.failed():
            return
        if not request.IsInitialized():
            controller.handleError(rpc_pb.BAD_REQUEST_PROTO, "Client requst not initialized.")

    def _send_rpc_request(self, rpcRequest):
        self.socket.send(rpcRequest.SerializeToString())

    def _create_rpc_request(self, method, request):
        rpcRequest = rpc_pb.Request()
        rpcRequest.request_proto = request.SerializeToString()
        rpcRequest.service_name = method.containing_service.full_name
        rpcRequest.method_name = method.name
        return rpcRequest

    def _recv_response(self):
        resp = self.socket.recv()
        return resp

    def _serialize_string(self, str_, serialize_class):
        obj_ = serialize_class()
        obj_.ParseFromString(str_)
        return obj_

