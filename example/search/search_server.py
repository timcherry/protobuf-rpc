from SearchService_pb2 import SearchService, SearchResponse
from zerorpc.server import ZeroMQServer
from tcprpc.server import RawTCPServer


class SearchImpl(SearchService):
    def Search(self, controller, request, done):
        print "QUERY:", request.query
        response = SearchResponse()
        response.response = "booooya"
        done.run(response)

RawTCPServer("127.0.0.1", 1234, SearchImpl()).serve_forever()
