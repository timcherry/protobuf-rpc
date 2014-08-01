from Queue import Queue

class ObjectPool(object):
    """
    TODOD: implement spin down of unused objects
    """
    def __init__(self, obj=None, size=None, maxsize=None, *args, **kwargs):
        self.queue = Queue(maxsize = maxsize)
        self.maxsize = maxsize
        self.size = size
        self.obj = obj
        self.args = args
        self.kwargs = kwargs
        [self.queue.put(obj(*self.args, **self.kwargs)) for i in range(size)]
        self.cursize = size


    def get(self, block=True, timeout=None):
        if self.queue.empty() and self.cursize < self.maxsize:
            print "CUR SIZE", self.cursize
            self.cursize += 1
            self.queue.put(self.obj(*self.args, **self.kwargs))
        return self.queue.get(block=block, timeout=timeout)

    def release(self, obj):
        assert isinstance(obj, self.obj)
        self.queue.put(obj)

