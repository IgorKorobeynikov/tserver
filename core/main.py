from abc import ABCMeta, abstractmethod, abstractproperty
from submodules.BList import BList
import socket


class BaseServer(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self): pass

    @abstractproperty
    def online(self): pass

    @abstractmethod
    def handle_request(self): pass


class Server(BaseServer):
    def __init__(self, port=9265, max_conns=10):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', port))
        self.clients = BList(15)
    
    @property
    def online(self):
        # Not implemented yet
        pass

    def handle_request(self, request):
        # Not implemented yet
        pass
