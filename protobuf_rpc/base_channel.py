from google.protobuf.service import RpcChannel
from protobuf_rpc.protos.rpc_pb2 import Request, Response, BAD_REQUEST_PROTO
from protobuf_rpc.util import serialize_string
from protobuf_rpc.error import ERROR_CODE_TO_ERROR_CLASS, NO_ERROR,ProtobufError

class ProtoBufRPCChannel(RpcChannel):

    def CallMethod(self, method, controller, request, response_class, done_callback):
        rpc_request = self.create_rpc_request(method, request)
        response = self.send_rpc_request(rpc_request)
        resp_obj = serialize_string(response, Response)
        self.check_for_errors(resp_obj)
        serialized_resp_obj = serialize_string(resp_obj.response_proto,
                                                     response_class)
        if done_callback:
            done_callback(serialized_resp_obj)
        else:
            return serialized_resp_obj

    def check_for_errors(self, resp_obj):
        if resp_obj.error_code == NO_ERROR:
            return
        error_class = ERROR_CODE_TO_ERROR_CLASS.get(resp_obj.error_code,
                                                    ProtobufError)
        error_message = getattr(resp_obj, "error_message", "RPC Error")
        raise error_class(error_message)



    def create_rpc_request(self, method, request):
        rpcRequest = Request()
        rpcRequest.request_proto = request.SerializeToString()
        rpcRequest.service_name = method.containing_service.full_name
        rpcRequest.method_name = method.name
        return rpcRequest



