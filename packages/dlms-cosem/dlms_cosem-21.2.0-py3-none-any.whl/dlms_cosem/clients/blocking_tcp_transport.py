import logging
import socket
from typing import *

import attr

from dlms_cosem import exceptions
from dlms_cosem.protocol.wrappers import WrapperHeader, WrapperProtocolDataUnit

LOG = logging.getLogger(__name__)


@attr.s(auto_attribs=True)
class BlockingTcpTransport:

    host: str
    port: int
    client_logical_address: int
    server_logical_address: int
    timeout: int = attr.ib(default=5)
    tcp_socket: Optional[socket.socket] = attr.ib(init=False, default=None)

    @property
    def address(self) -> Tuple[str, int]:
        return self.host, self.port

    def wrap(self, bytes_to_wrap: bytes) -> bytes:
        """
        When sending data over TCP or UDP it is necessary to wrap the data in the in
        the DLMS IP wrapper. This is so the server (meter) knows where the data is
        intended and how long the message is since there is no "final/poll" bit like
        in HDLC.
        """
        header = WrapperHeader(
            source_wport=self.client_logical_address,
            destination_wport=self.server_logical_address,
            length=len(bytes_to_wrap),
        )
        return WrapperProtocolDataUnit(bytes_to_wrap, header).to_bytes()

    def connect(self):
        """Create a new socket and set it on the transport"""
        try:
            self.tcp_socket = socket.create_connection(
                address=self.address, timeout=self.timeout
            )
        except (
            OSError,
            IOError,
            socket.timeout,
            socket.error,
            ConnectionRefusedError,
        ) as e:
            raise exceptions.CommunicationError("Unable to connect socket") from e
        LOG.info(f"Connected to {self.address}")

    def disconnect(self):
        """Close socket and remove it from the transport"""
        try:
            self.tcp_socket.close()
        except (OSError, IOError, socket.timeout, socket.error) as e:
            raise exceptions.CommunicationError from e
        self.tcp_socket = None

    def send(self, bytes_to_send: bytes) -> bytes:
        if not self.tcp_socket:
            raise RuntimeError("TCP transport not connected.")
        try:
            self.tcp_socket.sendall(self.wrap(bytes_to_send))
        except (OSError, IOError, socket.timeout, socket.error) as e:
            raise exceptions.CommunicationError("Could no send data") from e

        return self.recv()

    def recv(self) -> bytes:
        if not self.tcp_socket:
            raise RuntimeError("TCP transport not connected.")
        header = WrapperHeader.from_bytes(self.tcp_socket.recv(8))
        try:
            data = self.tcp_socket.recv(header.length)
        except (OSError, IOError, socket.timeout, socket.error) as e:
            raise exceptions.CommunicationError("Could not receive data") from e
        return data
