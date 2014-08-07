from protobuf_rpc.base_channel import ProtoBufRPCChannel
from protobuf_rpc.pool import ObjectPool
from protobuf_rpc.connection import ZMQConnection

class ZMQChannel(ProtoBufRPCChannel):
    def __init__(self, hosts, pool_size=10, max_pool_size=100):
        self.connection_pool = ObjectPool(ZMQConnection,
                                          size=pool_size,
                                          maxsize=max_pool_size,
                                          hosts=hosts)

    def send_rpc_request(self, request):
        with self.connection_pool.get() as con:
            error = None
            con.send(request.SerializeToString())
            try:
                resp = con.recv()
            except IOError as ioe:
                con.close()
                error = ioe
                raise ObjectPool.Remove
        if error is not None:
            raise error
        return resp
