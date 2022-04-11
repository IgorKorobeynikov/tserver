from json import dumps, loads
from json.decoder import JSONDecodeError
from typing import Any, Dict, NoReturn, Union, List, Tuple, Deque, BinaryIO, Callable
from queue import deque
from copy import deepcopy
from uuid import uuid4
from random import randint
from io import BytesIO
from hashlib import md5
from socket import timeout

from submodules import (
    BList, 
    ListBlockedError, 
    show_stat,
    Repeater, 
    UdpSocket
)

from core.Infrastructure import BaseServer
from submodules.base_types import *

from .base_logger import logger

STimeOutError = timeout

class Server(BaseServer):
    def __init__(self, port: int = 9265, max_conns: int = 100, chat_size: int = 10) -> None:
        self.transport: UdpSocket = UdpSocket()
        self.addreses: List[Tuple[str, int]] = []  # contains addresses of all connected clients
        self.port: int = port
        
        self.clients: BList[ClientData] = BList(max_conns)

        self.repeater: Repeater = Repeater(1, show_stat, self)
        self.buf_request: Any = None
        self.msg_buffer: Deque[list[str, str]] = deque(maxlen=chat_size)
        self.admin_key: str = uuid4().hex
        self.raw_map: BinaryIO = BytesIO()
        self.__is_run: bool = True

        self.init_map()
        self.transport.bind(("", port))
        self.transport.settimeout(1)

        self.requests: Dict[str, Callable] = {
            "get_online": self.get_online,
            "connect": self.connect,
            "disconnect": self.disconnect,
            "push_data": self.push_data,
            "get_data": self.get_data,
            "get_messages": self.get_messages,
            "push_message": self.push_message,
            "clear_chat": self.clear_chat,
            "get_map": self.get_map,
            "ping": self.pong,
        }

    def break_server(self) -> None:
        self.__is_run = False

    @staticmethod
    def emergencyExit() -> NoReturn:
        raise SystemExit(0)

    @property
    def is_running(self) -> bool:
        return self.__is_run

    def pong(self, request: ClientRequest) -> ServerResponse:
        response = {
            "status": 0, 
            "response": None
        }
        return response

    def init_map(self) -> None:

        for x in range(0, 3200, 64):
            for y in range(0, 3200, 64):

                i = randint(0, 3)

                self.raw_map.write(
                    b"".join(
                        [
                            i.to_bytes(1, "big"),
                            x.to_bytes(2, "big"),
                            y.to_bytes(2, "big"),
                        ]
                    )
                )

    def get_map(self, request: ClientRequest) -> ServerResponse:

        response = {
            "status": 0,
            "response": {
                "checksum": md5(self.raw_map.getvalue()).hexdigest(),
                "map": list(bytearray(self.raw_map.getvalue())),
            },
        }
        return response

    def clear_chat(self, request: ClientRequest) -> ServerResponse:

        if request["client_data"]["key"] == self.admin_key:
            self.msg_buffer.clear()
            # только админы могут чистить чат
            # only admins can clean the chat
            response = {
                "status": 0, 
                "response": None
            }
            return response

        response = {
            "status": -40, 
            "response": None
        }
        return response

    @staticmethod
    def reset_keys(data: List[ClientData]) -> List[ClientDataNullKeys]:
        data = deepcopy(data)
        for client_data in data:
            client_data["key"] = None
        return data

    def get_messages(self, request: ClientRequest) -> ServerResponse:
        response = {
            "status": 0,
            "response": list(self.msg_buffer)
        }
        return response

    def push_message(self, request: ClientRequest) -> ServerResponse:
        message = request["request_body"]["msg_content"]
        nick = request["request_body"]["nick"]
        if len(message):
            self.msg_buffer.append([message, nick])

            response = {"status": 0, "response": None}

            return response

    def push_data(self, request: ClientRequest) -> ServerResponse:
        id = request["client_data"]["id"]

        keyd = self.clients[request["client_data"]["id"]]["key"]  # key of user by id

        if keyd == request["client_data"]["key"]:
            self.clients[id]["player_data"] = request["player_data"]

            self.clients[id]["client_timeout_ms"] = request["client_data"][
                "client_timeout_ms"
            ]
            response = {
                "status": 0, 
                "response": None
                }
            return response
        else:
            response = {
                "status": -40, 
                "response": None
            }
            return response

    def get_data(self, request: ClientRequest) -> ServerResponse:
        response = {
            "status": 0, 
            "response": self.reset_keys(self.clients)
        }
        return response

    @property
    def online(self) -> int:
        return len(self.clients)

    def get_online(self, request: ClientRequest) -> ServerResponse:

        response = {
            "status": 0,
            "response": self.online
        }

        return response

    def connect(self, request: ClientRequest) -> ServerResponse:
        addres = request["client_data"]["addres"]

        if addres not in self.addreses:
            try:
                request["client_data"]["id"] = len(self.clients)

                response = {
                    "status": 0, 
                    "response": len(self.clients)
                }

                client_data = {
                    "key": request["client_data"]["key"],
                    "id": request["client_data"]["id"],
                    "addres": addres,
                    "client_timeout_ms": request["client_data"]["client_timeout_ms"],
                    "player_data": request["player_data"],
                }

                self.clients.append(client_data)
                self.addreses.append(addres)
                return response
            except ListBlockedError:
                response = {
                    "status": -1, 
                    "response": None
                }
                return response
        
        response = {
            "status": -22,
            "response": None
        }
        return response
    def disconnect(self, request: ClientRequest) -> ServerResponse:
        addres = request["client_data"]["addres"]
        try:
            keyd = self.clients[
                request["client_data"]["id"]][
                    "key"
            ]  # key of user by id

        except IndexError as exc:
            response = {
                "status": -20, 
                "response": None
            }

            return response

        except Exception as exc:
            response = {
                "status": -127, 
                "err_content": repr(exc), 
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

    def handle_request(self, request: ClientRequest) -> ServerResponse:
        return self.requests[request["request"]].__call__(request)

    def run(self) -> None:
        logger.info("Server is started")

        self.repeater.do()

        while self.is_running:

            try:
                raw_data, addres = self.transport.recvfrom(1024)
            except STimeOutError as exc:
                continue
            except Exception as exc:
                logger.error(repr(exc))
            try:
                request = loads(raw_data.decode())

                request["client_data"]["addres"] = addres

                self.transport.sendto(
                    dumps(self.handle_request(request)).encode(), addres
                )

            except JSONDecodeError as exc:
                response = {
                    "status": -3, 
                    "response": None
                }
                self.transport.sendto(dumps(response).encode(), addres)

            except Exception as exc:
                response = {
                    "status": -127, 
                    "err_content": repr(exc), 
                    "response": None
                }
                logger.error(repr(exc))
                self.transport.sendto(dumps(response).encode(), addres)
