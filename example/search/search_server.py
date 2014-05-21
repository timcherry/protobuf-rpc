from SearchService_pb2 import SearchService, SearchResponse
from server import SocketRpcServer

class SearchImpl(SearchService):
    def Search(self, controller, request, done):
        print "In Search!"

        print "QUERY:", request.query

        response = SearchResponse()
        response.response = "booooya"


        done.run(response)



srv = SocketRpcServer(1234)
srv.registerService(SearchImpl())

print "SERVING"
srv.run()
