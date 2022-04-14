from core.Infrastructure.base_transport import Transport
from .base_types import ClientRequest, ServerResponse
from .ext_socket import UdpSocket

from json import dumps, loads
from typing import _Alias, ByteString, Tuple


Port = _Alias(int)
ClAddres = Tuple[str, Port]
BytesAmount = _Alias(int)

class UdpSocket(UdpSocket, Transport):
    def __init__(self):
        super().__init__()

    def sendto(self, packet: ServerResponse, addres: ClAddres) -> int:

        raw_packet: ByteString = dumps(packet).encode()

        self.__total_sent += len(raw_packet)
        return super().sendto(raw_packet, addres)

    def recvfrom(self, buffersize: int) -> Tuple[ClientRequest, ClAddres]:
        raw_packet, addr = super().recvfrom(buffersize)
        raw_packet: ByteString = raw_packet
        addres: ClAddres = addr

        self.__total_recv += len(raw_packet)

        packet: ClientRequest = loads(raw_packet.decode())

        return packet, addres
