import logging
import socket
from typing import Optional

from config import (
    COMMAND_SPLITTER,
    CONNECT_TIMEOUT,
    SERVER_IP_CONNECT,
    SERVER_PORT,
    ControlParam,
)
from robohandcontrol.robocontrol import RobohandControlBase

log = logging.getLogger(__name__)


class RobohandControlClientSocket(RobohandControlBase):
    def __init__(
        self,
        server_host: str = SERVER_IP_CONNECT,
        server_port: int = SERVER_PORT,
        command_splitter: str = COMMAND_SPLITTER,
    ) -> None:
        self.server_host = server_host
        self.server_port = server_port
        self.command_splitter = command_splitter
        self._socket: Optional[socket.socket] = None

    def control_claw(self, angle: int) -> None:
        log.info("[Send] Set claw angle to %s", angle)
        self.send_command(ControlParam.CLAW, angle)

    def control_extend_arrow(self, angle: int) -> None:
        log.info("[Send] Extend tower to angle %s", angle)
        self.send_command(ControlParam.EXTEND_ARROW, angle)

    def control_raise_arrow(self, angle: int) -> None:
        log.info("[Send] Raise tower to angle %s", angle)
        self.send_command(ControlParam.RAISE_ARROW, angle)

    def control_rotation(self, angle: int) -> None:
        log.info("[Send] Rotate base to angle %s", angle)
        self.send_command(ControlParam.ROTATION, angle)

    def set_led_rgb(self, red: int, green: int, blue: int) -> None:
        log.info("[Send] Set led rgb to %s, %s, %s", red, green, blue)
        self.send_command(ControlParam.LED, red, green, blue)

    @property
    def socket(self) -> Optional[socket.socket]:
        """
        :return:
        """
        if self._socket:
            return self._socket
        log.debug("Create a TCP socket")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(CONNECT_TIMEOUT)

        try:
            log.debug("Connect to the server")
            client_socket.connect((SERVER_IP_CONNECT, SERVER_PORT))
        except socket.timeout:
            log.error(
                "Connection to %s:%s timed out after %s seconds",
                SERVER_IP_CONNECT,
                SERVER_PORT,
                CONNECT_TIMEOUT,
            )
            return None
        except OSError as e:
            log.error("Could not connect to host, error: %s", e)
        except ConnectionRefusedError:
            log.error(
                "Could not connect to server %s:%s",
                self.server_host,
                self.server_port,
            )
            return None
        self._socket = client_socket
        return self._socket

    def send_command_to_server(self, command: str) -> None:
        if not self.socket:
            return

        try:
            self.socket.send(command.encode("utf-8"))
        except TimeoutError:
            log.error("Server socket connection timed out")
            self._socket = None
        except BrokenPipeError:
            log.error(
                "Connection refused on server %s:%s, skip sending command %r",
                self.server_host,
                self.server_port,
                command,
            )
            self._socket = None

    def send_command(self, prefix: str, *args: int) -> None:
        command = self.command_splitter.join((prefix, *map(str, args))) + ";"
        self.send_command_to_server(command)
