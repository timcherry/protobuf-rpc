from SearchService_pb2 import SearchService_Stub, SearchService, SearchRequest
from zerorpc.channel import ZeroMQChannel
from controller import SocketRpcController



channel = ZeroMQChannel(host='localhost', port=1234)
service = SearchService_Stub(channel)
controller = SocketRpcController()

request = SearchRequest()
request.query = "tim"
SearchService_Stub.Search(service, controller, request)


req = SearchRequest()
req.query = "foopoo"
SearchService_Stub.Search(service, controller, req)



