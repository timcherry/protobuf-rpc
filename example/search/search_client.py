from SearchService_pb2 import SearchService_Stub, SearchService, SearchRequest
from channel import SocketRpcChannel

request = SearchRequest()
request.query = "tim"

channel = SocketRpcChannel(host='localhost', port=1234)
service = SearchService_Stub(channel)
controller = channel.newController()


SearchService_Stub.Search(service, controller, request)

