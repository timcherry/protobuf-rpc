import zmq

from SearchService_pb2 import SearchService_Stub, SearchRequest
from protobuf_rpc.channel import ZeroMQChannel
from protobuf_rpc.controller import SocketRpcController



def callback(response):
    print "Server response", response.response


ctx = zmq.Context() # create a new context to kick the wheels
sock = ctx.socket(zmq.REQ)
sock.connect('tcp://127.0.0.1:1234')


channel = ZeroMQChannel(host="127.0.0.1", port=1234)
service = SearchService_Stub(channel)
controller = SocketRpcController()

request = SearchRequest()
request.query = "tim"
SearchService_Stub.Search(service, controller, request, callback=callback)


req = SearchRequest()
req.query = "foopoo"
SearchService_Stub.Search(service, controller, req)



