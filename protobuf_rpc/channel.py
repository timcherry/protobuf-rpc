import zmq.green as zmq
# import zmq
from protobuf_rpc.base_channel import ProtoBufRPCChannel
from protobuf_rpc.pool import ObjectPool, ZMQConnection

class ZeroMQChannel(ProtoBufRPCChannel):
    def __init__(self, hosts):
        self.connection_pool = ObjectPool(ZMQConnection,
                                          size=10,
                                          maxsize=100,
                                          hosts=hosts)

    def send_rpc_request(self, request):

        try:
            con = self.connection_pool.get()
            con.send(request.SerializeToString())
            resp = con.recv()
        except Exception as e:
            print "ERROR",e
        finally:
            if con:
                self.connection_pool.release(con)
        return resp

