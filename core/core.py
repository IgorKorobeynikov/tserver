from abc import ABCMeta, abstractmethod
import socket


class BaseServer(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    def get_online(self): pass

    @abstractmethod
    def handle_request(self): pass


class Server(BaseServer):
    def __init__(self, port=9265, max_conns=10):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', port))
        self.clients = deque(maxlen=max_conns)

    def get_online(self):
        # Not implemented yet
        pass

    def handle_request(self, request):
        # Not implemented yet
        pass
