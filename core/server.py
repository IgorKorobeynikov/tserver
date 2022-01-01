from json import dumps, loads
from json.decoder import JSONDecodeError
from typing import Union
from queue import deque
import socket

from submodules import BList, ListBlockedError, show_stat, Repeater, UdpSocket
from core.Infrastructure import BaseServer


class Server(BaseServer):
    def __init__(self, port=9265, max_conns=100, chat_size=10):
        self.socket = UdpSocket()
        self.addreses = []  # contains addresses of all connected clients
        self.port = port
        self.socket.bind(("", port))
        self.clients = BList(max_conns)
        self.repeater = Repeater(1, show_stat, self)
        self.buf_request = None
        self.msg_buffer = deque(maxsize=chat_size)
        self.requests = {
            "get_online": self.get_online,
            "connect": self.connect,
            "disconnect": self.disconnect,
            "push_data": self.push_data,
            "get_data": self.get_data
        }

    def get_messages(self, request: dict):
        response = {
            "status": 0,
            "response": list(self.msg_buffer)
        }
        return response

    def push_message(self, request: dict) -> dict:
        message = request['request_body']['msg_content']
        nick = request['request_body']['nick']
        if len(message):
            self.msg_buffer.append([message, nick])

            response = {
                "status": 0,
                "response": None

            }

            return response

    def push_data(self, request: dict) -> dict:
        id = request['client_data']['id']

        keyd = self.clients[request["client_data"]["id"]][
            "key"
        ]  # key of user by id

        if keyd == request["client_data"]["key"]:
            self.clients[id]['posx'] = request['request_body']['posx']
            self.clients[id]['posy'] = request['request_body']['posy']
            self.clients[id]['rot'] = request['request_body']['rot']
            self.clients[id]['turret_rot'] = request['request_body']['turret_rot']
            response = {
                "status": 0,
                "response": None
            }
            return response
        else:
            response = {
                "status": -127,
                "response": None
            }
            return response

    def get_data(self, request: dict) -> dict:
        response = {
            "status": 0,
            "response": self.clients
        }
        return response

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

    def handle_request(self, request: dict) -> Union[dict, BList]:
        return self.requests[request["request"]].__call__(request)

    def run(self):
        self.repeater.do()
        while True:

            raw_data, addres = self.socket.recvfrom(1024)

            try:
                request = loads(raw_data.decode())

                request["client_data"]["addres"] = addres

                self.socket.sendto(
                    dumps(self.handle_request(request)).encode(), addres
                )
            except JSONDecodeError:
                response = {
                    "status": -3,
                    "response": None
                }

                self.socket.sendto(dumps(response).encode(), addres)

            except Exception:
                response = {
                    "status": -127,
                    "response": None
                }

                self.socket.sendto(dumps(response).encode(), addres)
