from unittest import mock

from pytest_mock import MockerFixture

from config.di import Container
from dnsclient.client import DNSClient
from utils.entities import DNSResponse


class TestDNSClient:
    def setup_method(self):
        self.dnsresponse = DNSResponse(
            code=0, domain_name="example.com", ip="2.2.2.2", error=None
        )
        self.ip = "1.1.1.1"
        self.port = 1
        self.packet = mock.Mock(return_value=b"packet")
        self.handler = mock.Mock(return_value=self.dnsresponse)

        self.socket = mock.Mock()
        self.socket.recvfrom.return_value = "content", "address"

        self.context = Container.dns_client.override(
            DNSClient(
                ip=self.ip,
                port=self.port,
                packet=self.packet,
                handler=self.handler,
            )
        )

    def test_send(self, mocker: MockerFixture):
        socket = mocker.patch("dnsclient.client.socket")
        socket.socket.return_value = self.socket
        socket.AF_INET = "AF_INET"
        socket.SOCK_DGRAM = "SOCK_DGRAM"
        with self.context:
            packet = Container.dns_client().send("content")

            assert packet == self.packet
            socket.socket.assert_called_once_with("AF_INET", "SOCK_DGRAM")
            self.socket.sendto.assert_called_once_with(
                self.packet.return_value, (self.ip, self.port)
            )
            self.socket.recvfrom.assert_not_called()
            self.packet.assert_called_once_with("content")
            self.handler.assert_not_called()

    def test_recieve(self, mocker: MockerFixture):
        socket = mocker.patch("dnsclient.client.socket")
        socket.socket.return_value = self.socket
        socket.AF_INET = "AF_INET"
        socket.SOCK_DGRAM = "SOCK_DGRAM"
        with self.context:
            response = Container.dns_client().recieve(self.packet)

            assert response == self.dnsresponse
            socket.socket.assert_called_once_with("AF_INET", "SOCK_DGRAM")
            self.socket.sendto.assert_not_called()
            self.socket.recvfrom.assert_called_once_with(DNSClient.READ_BUFFER)
            self.packet.assert_not_called()
            self.handler.assert_called_once_with("content", self.packet)
