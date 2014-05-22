from SearchService_pb2 import SearchService_Stub, SearchService, SearchRequest
from zerorpc.channel import ZeroMQChannel
from common.controller import SocketRpcController

def callback(response):
    print "Server response", response.response

channel = ZeroMQChannel(host='localhost', port=1234)
service = SearchService_Stub(channel)
controller = SocketRpcController()

request = SearchRequest()
request.query = "tim"
SearchService_Stub.Search(service, controller, request, callback=callback)


req = SearchRequest()
req.query = "foopoo"
SearchService_Stub.Search(service, controller, req)



