from gevent import monkey
monkey.patch_all()

import gevent

from SearchService_pb2 import SearchService_Stub, SearchRequest
from protobuf_rpc.channel import ZMQChannel
from protobuf_rpc.controller import SocketRpcController
import time

def callback(response):
    print "Server response", response.response

channel = ZMQChannel(hosts=[("127.0.0.1", 1234),
                            ("127.0.0.1", 12345),
                            ("127.0.0.1", 123456)])

service = SearchService_Stub(channel)
controller = SocketRpcController()

def send_requests(thread_id):

    request = SearchRequest()
    request.query = "tim"
    print 'Thread %s, Sending Request 1'%(thread_id)
    SearchService_Stub.Search(service, controller, request, callback=callback)



    req = SearchRequest()
    req.query = "tim2"
    print 'Thread %s, Sending Request 2'%(thread_id)
    SearchService_Stub.Search(service, controller, req, callback=callback)


    req = SearchRequest()
    req.query = "tim3"
    print 'Thread %s, Sending Request 3'%(thread_id)
    SearchService_Stub.Search(service, controller, req, callback=callback)

    req = SearchRequest()
    req.query = "tim4"
    print 'Thread %s, Sending Request 4'%(thread_id)
    SearchService_Stub.Search(service, controller, req, callback=callback)



def run():
    greens = []
    for x in range(1, 100):
        greens.append(gevent.spawn(send_requests, x))
        time.sleep(1)
    gevent.joinall(greens)


if __name__ == "__main__":
    run()
