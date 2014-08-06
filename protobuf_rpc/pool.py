from Queue import Queue
from contextlib import contextmanager



class ObjectPool(object):
    """
    TODOD: implement spin down of unused objects
    """

    class Remove(Exception):
        pass

    def __init__(self, obj=None, size=None, maxsize=None, *args, **kwargs):
        self.queue = Queue(maxsize = maxsize)
        self.maxsize = maxsize
        self.size = size
        self.obj = obj
        self.args = args
        self.kwargs = kwargs
        [self.queue.put(obj(*self.args, **self.kwargs)) for i in range(size)]
        self.cursize = size

    @contextmanager
    def get(self, block=True, timeout=None):
        try:
            obj = self._get(block, timeout)
            yield obj
            self.release(obj)
        except self.Remove:
            self.remove(obj)
        except Exception as e:
            self.release(obj)
            raise e

    def remove(self, obj):
        print "RELEASING1234"
        self.cursize -= 1
        print "QUEUE SIZE", self.queue.qsize()

    def _get(self, block, timeout):
        if self.queue.empty() and self.cursize < self.maxsize:
            self.cursize += 1
            self.queue.put(self.obj(*self.args, **self.kwargs))
        return self.queue.get(block=block, timeout=timeout)

    def release(self, obj):
        assert isinstance(obj, self.obj)
        self.queue.put(obj)

