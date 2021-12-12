from abc import ABCMeta, abstractmethod, abstractproperty
from submodules import BList
import socket


class BaseServer(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self): pass

    @abstractproperty
    def online(self): pass

    @abstractmethod
    def handle_request(self): pass

    @abstractmethod
    def run(self): pass


class Server(BaseServer):
    def __init__(self, port=9265, max_conns=10):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', port))
        self.clients = BList(max_conns)

    @property
    def online(self):
        # Not implemented yet
        pass

    def handle_request(self, request):
        pass

    def run(self):
        while True:
            raw_data, addres = self.socket.recvfrom(1024)
            data = raw_data.decode()

            if addres not in self.clients:
                self.clients.append(addres)

            if data == "disconnect":
                self.clients.remove(addres)
                continue

            if data == "req{get_online}":
                self.socket.sendto(str(self.online).encode("ascii"), addres)

            for client in self.clients:
                if client == addres:
                    continue
                self.socket.sendto(raw_data, client)
