import socket
from typing import Dict
from dns_client.UDP import UDP
from dns_client.exceptions import ValidationError


class Client:
    DNS_IP = '8.8.8.8'  # Google public DNS server IP.
    DNS_PORT = 53  # DNS server port for queries.
    READ_BUFFER = 1024  # The size of the buffer to read in the received UDP packet.

    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Address family: Internet, type: UDP
        self.udp = None

    def send(self, domain_name: str) -> None:
        """Send the packet to the server"""
        self.udp = UDP(message=domain_name)
        self.__send_dns_query(
            self.udp.builded_request,
            (self.DNS_IP, self.DNS_PORT)
        )

    def recieve(self) -> Dict:
        """
        Recieve response DNS packet back. 
        Return validated response data
        """
        if not self.udp:
            raise ValidationError("You must send dns query before trying to recieve any response")
        data, address = self.__recieve_data()
        self.udp.validate(data)

        return self.udp.validated_response

    def __send_dns_query(self, udp: bytes, address: tuple) -> None:
        self.client.sendto(udp, address)

    def __recieve_data(self) -> tuple:
        return self.client.recvfrom(self.READ_BUFFER)