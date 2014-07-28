import google.protobuf.service as service
import protobuf_rpc.protos.rpc_pb2 as rpc_pb
from protobuf_rpc.common.util import serialize_string

class ProtoBufRPCChannel(service.RpcChannel):

    def CallMethod(self, method, controller, request, response_class, done):
        self.validate_requst(controller, request)
        rpc_request = self.create_rpc_request(method, request)
        self.send_rpc_request(rpc_request)
        response = self.recv_response()
        resp_obj = serialize_string(response, rpc_pb.Response)
        serialized_resp_obj = serialize_string(resp_obj.response_proto,
                                                     response_class)
        if done:
            done(serialized_resp_obj)

    def validate_requst(self, controller, request):
        if controller.failed():
            return
        if not request.IsInitialized():
            controller.handleError(rpc_pb.BAD_REQUEST_PROTO, "Client requst not initialized.")

    def create_rpc_request(self, method, request):
        rpcRequest = rpc_pb.Request()
        rpcRequest.request_proto = request.SerializeToString()
        rpcRequest.service_name = method.containing_service.full_name
        rpcRequest.method_name = method.name
        return rpcRequest



