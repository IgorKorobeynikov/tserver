from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Tuple, _Alias

Port = _Alias(int)
ClAddres = Tuple[str, Port]
BytesAmount = _Alias(int)

class Transport(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self) -> None:
        ...
    @abstractmethod
    def listen(self, buffsize: int, encoding: str) -> Tuple[str, ClAddres]:
        ...
    @abstractmethod
    def sendto(self, content: str, addr: ClAddres) -> BytesAmount:
        ...
    @abstractproperty
    def total_sent(self) -> BytesAmount:
        ...
    @abstractproperty
    def total_recv(self) -> BytesAmount:
        ...
    