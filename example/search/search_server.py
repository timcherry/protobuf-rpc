from gevent import monkey
monkey.patch_all()

from SearchService_pb2 import SearchService, SearchResponse
from protobuf_rpc.server import GServer


class SearchImpl(SearchService):
    def Search(self, controller, request, done):
        print "QUERY:", request.query
        response = SearchResponse()
        response.response = "booooya"
        done.run(response)

GServer("*", 1234, SearchImpl()).serve_forever()