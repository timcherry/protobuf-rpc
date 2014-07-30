from google.protobuf.service import RpcController


class SocketRpcController(RpcController):
    ''' RpcController implementation to be used by the SocketRpcChannel class.

    The RpcController is used to mediate a single method call.
    '''

    def __init__(self):
        '''Constructor which initializes the controller's state.'''
        self._fail = False
        self._error = None
        self.reason = None

    def handleError(self, error_code, message):
        '''Log and set the controller state.'''
        self._fail = True
        self.reason = error_code
        self._error = message

    def reset(self):
        '''Resets the controller i.e. clears the error state.'''
        self._fail = False
        self._error = None
        self.reason = None

    def failed(self):
        '''Returns True if the controller is in a failed state.'''
        return self._fail

    def error(self):
        return self._error
