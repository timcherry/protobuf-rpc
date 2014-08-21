from gevent import monkey
monkey.patch_all()

import zmq.green as zmq
from protobuf_rpc.connection import ZMQConnection
import unittest

class TestConnection(unittest.TestCase):

    def setUp(self,):
        ctx1 = zmq.Context()
        self.serv_con1 = ctx1.socket(zmq.ROUTER)
        self.serv_con1.bind("tcp://127.0.0.1:12345")
        self.hosts = [("127.0.0.1",12345)]
        self.con = ZMQConnection(self.hosts)

    def tearDown(self):
        self.con.close()
        self.serv_con1.close()

    def test_send(self):
        mock_msg = "PING"
        self.con.send(mock_msg)
        msg1 = self.serv_con1.recv_multipart()
        self.assertEquals(msg1[2], mock_msg)

    def test_send_recv(self):
        self.hosts = [("127.0.0.1",12345)]
        self.con = ZMQConnection(self.hosts)
        mock_msg = "PING"
        self.con.send(mock_msg)
        [id_, null, req] = self.serv_con1.recv_multipart()
        self.assertEquals(req, mock_msg)
        mock_resp = "PONG"
        self.serv_con1.send_multipart([id_, null, mock_resp])
        resp = self.con.recv()
        self.assertEquals(resp, mock_resp)

    def test_timeout(self,):
        self.hosts = [("127.0.0.1",12345)]
        self.con = ZMQConnection(self.hosts)
        mock_msg = "PING"
        self.con.send(mock_msg)
        [id_, null, req] = self.serv_con1.recv_multipart()
        self.assertEquals(req, mock_msg)
        self.assertRaises(IOError, self.con.recv, 1)
