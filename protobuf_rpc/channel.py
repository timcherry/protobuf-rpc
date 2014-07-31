from protobuf_rpc.base_channel import ProtoBufRPCChannel
from protobuf_rpc.pool import ObjectPool
from protobuf_rpc.connection import ZMQConnection

class ZMQChannel(ProtoBufRPCChannel):
    def __init__(self, hosts):
        self.connection_pool = ObjectPool(ZMQConnection,
                                          size=10,
                                          maxsize=100,
                                          hosts=hosts)

    def send_rpc_request(self, request):
        con = self.connection_pool.get()
        con.send(request.SerializeToString())
        resp = con.recv()
        self.connection_pool.release(con)
        return resp

