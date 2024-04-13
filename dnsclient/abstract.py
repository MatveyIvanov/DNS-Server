from abc import ABC, abstractmethod
from socket import socket
from typing import TypeVar, Generic


T = TypeVar("T")
V = TypeVar("V")
G = TypeVar("G")


class CLI(ABC):
    @abstractmethod
    def run(self, args) -> None: ...


class Query(ABC, Generic[T, V]):
    @abstractmethod
    def __call__(self, entry: T) -> V | None: ...


class Client(ABC, Generic[T, V, G]):
    _client: socket | None
    READ_BUFFER: int

    @property
    @abstractmethod
    def client(self) -> socket: ...

    @abstractmethod
    def send(self, content: T) -> G: ...

    @abstractmethod
    def recieve(self, packet: G) -> V: ...

    def _send(self, packet: bytes, address: tuple) -> None:
        self.client.sendto(packet, address)

    def _recieve(self) -> tuple:
        return self.client.recvfrom(self.READ_BUFFER)


class UDPPacket(ABC, Generic[T, V]):
    content: V

    @abstractmethod
    def __call__(self, content: T) -> bytes: ...


class UDPHandler(ABC, Generic[G, V]):
    @abstractmethod
    def __call__(self, content: bytes, packet: G) -> V: ...
