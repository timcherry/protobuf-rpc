from gevent import monkey
monkey.patch_all()

from gevent.pool import Pool
import time
from protobuf_rpc.pool import ObjectPool
from protobuf_rpc.connection import ZMQConnection
import requests
import GreenletProfiler

http_session = requests.Session()

adapter = requests.adapters.HTTPAdapter(pool_connections=10,
                                        pool_maxsize=10,
                                        pool_block=True)
http_session.mount('http://', adapter)

http_url = "http://127.0.0.1:5001/ping"

gpool = Pool(100)

hosts = [('127.0.0.1', 12345)]

rpc_pool = ObjectPool(ZMQConnection,
                      size=10,
                      maxsize=10,
                      hosts=hosts)


NUM_REQUESTS = 10 * 1000

def http_hammer():
    r = http_session.get(http_url)
    assert r.text == 'pong'

def rpc_hammer():
    con = rpc_pool.get()
    con.send("ping")
    resp = con.recv()
    assert resp == 'pong'
    rpc_pool.release(con)


def run_hammer(hammer_func):
    start_time = time.time()
    for x in range(1, NUM_REQUESTS):
        gpool.spawn(hammer_func)
    gpool.join()
    end_time = time.time()
    elapsed = end_time - start_time
    average = elapsed / NUM_REQUESTS
    print "\tTotal Elapsed time:",(elapsed)
    print "\ttAverage Request time:",(average)


def run():
    print "Running ZMQ RPC HAMMER"
    #GreenletProfiler.set_clock_type('cpu')
    #GreenletProfiler.start()
    run_hammer(rpc_hammer)
    print "Sleeping"
    time.sleep(20)
    print "Running HTTP HAMMER"
    run_hammer(http_hammer)
    #GreenletProfiler.stop()
    #stats = GreenletProfiler.get_func_stats()
    #stats.print_all()
    #stats.save('hammer.callgrind', type='callgrind')

if __name__ == '__main__':
    run()
