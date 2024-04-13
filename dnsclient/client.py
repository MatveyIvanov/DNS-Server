import socket

from dnsclient.abstract import Client
from dnsclient.udp import UDPPacket, UDPHandler, DNSPacket
from utils.entities import DNSResponse


class DNSClient(Client[str, DNSResponse, DNSPacket]):
    _client: socket.socket | None = None
    READ_BUFFER: int = (
        1024  # The size of the buffer to read in the received UDP packet.
    )

    def __init__(
        self,
        ip: str,
        port: int,
        packet: UDPPacket,
        handler: UDPHandler,
    ) -> None:
        self.ip = ip
        self.port = port
        self.packet = packet
        self.handler = handler

    @property
    def client(self) -> socket.socket:
        if not self._client:
            self._client = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM
            )  # Address family: Internet, type: UDP
        return self._client

    def send(self, content: str) -> DNSPacket:
        """Send the packet to the server"""
        self._send(self.packet(content), (self.ip, self.port))
        return self.packet  # type: ignore

    def recieve(self, packet: DNSPacket) -> DNSResponse:
        """
        Recieve response DNS packet back.
        Return validated response data
        """
        content, address = self._recieve()
        return self.handler(content, packet)
