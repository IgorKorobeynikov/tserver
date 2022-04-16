from core.Infrastructure.base_transport import Transport
from .base_types import ClientRequest, ServerResponse
from .ext_socket import UdpSocket

from json import dumps, loads
from typing import ByteString, Dict, Tuple


Port = int
ClAddres = Tuple[str, Port]
BytesAmount = int
Packet = Dict # Will replaced in future

class UdpTransport(UdpSocket, Transport):
    def __init__(self):
        self.__total_recv = 0
        self.__total_sent = 0
        super().__init__()
    def sendto(self, packet: Packet, addres: ClAddres) -> int:

        raw_packet: ByteString = dumps(packet).encode()

        self.__total_sent += len(raw_packet)
        return super().sendto(raw_packet, addres)

    def recvfrom(self, buffersize: int) -> Tuple[Packet, ClAddres]:
        raw_packet, addr = super().recvfrom(buffersize)
        raw_packet: ByteString = raw_packet
        addres: ClAddres = addr

        self.__total_recv += len(raw_packet)

        packet: ClientRequest = loads(raw_packet.decode())

        return packet, addres
