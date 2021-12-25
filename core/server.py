from submodules import BList, ListBlockedError, show_stat, Timer, Repeater, UdpSocket
import socket
from core.Infrastructure import BaseServer
from json import dumps, loads


class Server(BaseServer):
    def __init__(self, port=9265, max_conns=2):
        self.socket = UdpSocket()  # socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addreses = []  # contains addresses of all conn clients
        self.port = port
        self.socket.bind(("", port))
        self.clients = BList(max_conns)
        self.repeater = Repeater(3, show_stat, self)
        self.buf_request = None
        self.requests = {
            "get_online": self.get_online,
            "connect": self.connect,
            "disconnect": self.disconnect,
        }

    @property
    def online(self) -> int:
        return len(self.clients)

    def get_online(self, *args, **kwargs) -> dict:

        response = {
            "status": 0,
            "response": self.online
        }

        return response

    def connect(self, request: dict) -> dict:
        addres = request["client_data"]["addres"]

        if addres not in self.addreses:
            try:
                request["client_data"]["id"] = len(self.clients)

                response = {
                    "status": 0,
                    "response": len(self.clients)
                }

                self.clients.append(request["client_data"])
                self.addreses.append(addres)
                return response
            except ListBlockedError:
                response = {
                    "status": -1,
                    "response": None
                }
                return response

    def disconnect(self, request: dict) -> dict:
        addres = request["client_data"]["addres"]
        try:
            keyd = self.clients[request["client_data"]["id"]][
                "key"
            ]  # key of user by id

        except IndexError as Error:
            response = {
                "status": -20,
                "response": None
            }

            return response

        except Exception as Error:
            response = {
                "status": -127,
                "response": None
            }

            return response

        if keyd == request["client_data"]["key"]:
            del self.clients[request["client_data"]["id"]]

            self.addreses.remove(addres)

            response = {
                "status": 0,
                "response": None
            }

            return response

        else:
            response = {
                "status": -21,
                "response": None
            }

            return response

    def handle_request(self, request: dict) -> dict:
        return self.requests[request["request"]].__call__(request)

    def run(self):
        self.repeater.do()
        while True:

            raw_data, addres = self.socket.recvfrom(1024)
            request = loads(raw_data.decode())
            request["client_data"]["addres"] = addres

            self.socket.sendto(
                dumps(self.handle_request(request)).encode(), addres
            )
