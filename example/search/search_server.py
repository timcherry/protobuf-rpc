from gevent import monkey
monkey.patch_all()

import gevent
from SearchService_pb2 import SearchService, SearchResponse
from protobuf_rpc.server import GServer


class SearchImpl(SearchService):
    def Search(self, controller, request, done):
        print "QUERY:", request.query
        response = SearchResponse()
        response.response = "booooya"
        done.run(response)

g1 = GServer("*", 1234, SearchImpl())
t1 =gevent.spawn(g1.serve_forever)


g2 = GServer("*", 12345, SearchImpl())
t2 = gevent.spawn(g2.serve_forever)

g3 = GServer("*", 123456, SearchImpl())
t3 = gevent.spawn(g3.serve_forever)

#import time; time.sleep(1)

#g1.shutdown()

gevent.joinall([t2, t2, t3])