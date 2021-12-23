from submodules import BList, ListBlockedError, show_stat, Timer
import socket
from core.Infrastructure import BaseServer
from json import dumps, loads


class Server(BaseServer):
    def __init__(self, port=9265, max_conns=2):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addreses = []  # contains addresses of all conn clients
        self.port = port
        self.socket.bind(('', port))
        self.clients = BList(max_conns)
        self.total_recv = 0
        self.total_sent = 0
        self.timer = Timer()

    @property
    def online(self) -> int:
        return len(self.clients)

    def handle_request(self, request: str):
        pass

    def run(self):
        while True:
            if round(self.timer.elsaped) % 2 == 0:
                show_stat(self)

            raw_data, addres = self.socket.recvfrom(1024)
            data = loads(raw_data.decode())
            data['client_data']['addres'] = addres

            self.total_recv += data.__sizeof__()

            # id клиента совпадает с идексом в массиве клиентов
            if data['request'] == "connect":
                if addres not in self.addreses:
                    try:
                        data['client_data']['id'] = len(self.clients)

                        response = dumps({
                            "status": 0,
                            "response": len(self.clients)
                        })

                        self.clients.append(data['client_data'])
                        self.addreses.append(addres)
                        self.socket.sendto(response.encode(), addres)

                    except ListBlockedError:
                        response = dumps({
                            "status": -1,
                            "response": None
                        })
                        self.socket.sendto(response.encode(), addres)
                continue
            if data['request'] == "disconnect":
                try:
                    keyd = self.clients[data['client_data']
                                        ['id']]['key']  # key of user by id

                except IndexError as Error:
                    response = dumps(
                        {
                            "status": -20,
                            "response": None
                        }
                    )

                    self.socket.sendto(response.encode(), addres)
                    continue

                except Exception as Error:
                    response = dumps(
                        {
                            "status": -127,
                            "response": None
                        }
                    )
                    self.socket.sendto(response.encode(), addres)
                    continue

                if keyd == data['client_data']['key']:
                    del(self.clients[
                        data['client_data']['id']
                    ])

                    self.addreses.remove(addres)

                    response = dumps(
                        {
                            "status": 0,
                            "response": None
                        }
                    )

                    self.socket.sendto(response.encode(), addres)

                else:
                    response = dumps(
                        {
                            "status": -21,
                            "response": None
                        }
                    )

                    self.socket.sendto(response.encode(), addres)
                continue

            if data['request'] == "get_online":

                response = dumps(
                    {
                        "status": 0,
                        "response": self.online
                    }
                ).encode()

                self.socket.sendto(response, addres)
                self.total_sent += response.__sizeof__()
                continue
