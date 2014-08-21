import unittest
from protobuf_rpc.pool import ObjectPool

class MockClass(object):
    def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar

class TestObjectPool(unittest.TestCase):
    def setUp(self):
        self.size = 5
        self.maxsize = 10
        self.pool = ObjectPool(MockClass,
                          size=self.size,
                          maxsize=self.maxsize,
                          foo="foo",
                          bar="bar")


    def test_init_size(self):
        self.assertEquals(self.pool.queue.qsize(),
                          self.size)
        self.assertEquals(self.pool.size,
                          self.size)


    def test_kwargs(self,):
        with self.pool.get(block=False) as obj:
            self.assertEquals(obj.foo, "foo")
            self.assertEquals(obj.bar, "bar")

    def test_args(self, ):
        self.pool = ObjectPool(MockClass,
                               self.size,
                               self.maxsize,
                               "foo",
                               "bar")
        with self.pool.get(block=False) as obj:
            self.assertEquals(obj.foo, "foo")
            self.assertEquals(obj.bar, "bar")

