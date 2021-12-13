from submodules import BList, show_stat
import socket
from core.Infrastructure import BaseServer


class Server(BaseServer):
    def __init__(self, port=9265, max_conns=10):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = port
        self.socket.bind(('', port))
        self.clients = BList(max_conns)
        self.total_recv = 0
        self.total_sent = 0

    @property
    def online(self) -> int:
        return len(self.clients)

    def handle_request(self, request: str):
        pass

    def run(self):
        while True:

            show_stat(self.port, self.clients, self.clients.capacity)

            raw_data, addres = self.socket.recvfrom(1024)
            data = raw_data.decode()

            if addres not in self.clients:
                self.clients.append(addres)

            if data == "disconnect":
                self.clients.remove(addres)
                continue

            if data == "req{get_online}":
                to_send = str(self.online).encode("ascii")
                self.socket.sendto(to_send, addres)
                self.total_sent += to_send.__sizeof__()
                continue

            for client in self.clients:
                if client == addres:
                    continue
                to_send = (raw_data, client)
                self.socket.sendto(*to_send)
                self.total_sent += to_send.__sizeof__()
