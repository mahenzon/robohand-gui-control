import logging
import select
import socket
from typing import TYPE_CHECKING

from config import (
    COMMAND_SPLITTER,
    COMMAND_ENDL,
    SERVER_IP_BIND,
    SERVER_PORT,
    ControlParam,
)
from robohandcontrol.robocontrol import RobohandControlBase

if TYPE_CHECKING:
    from typing import Callable

    # set angle or set rgb
    MethodType = Callable[[int], None] | Callable[[int, int, int], None]

log = logging.getLogger(__name__)


class RobohandControlServerSocket(RobohandControlBase):
    def __init__(
        self,
        robohand: RobohandControlBase,
        server_host: str = SERVER_IP_BIND,
        server_port: int = SERVER_PORT,
        command_splitter: str = COMMAND_SPLITTER,
    ) -> None:
        self.robohand = robohand
        self.server_host = server_host
        self.server_port = server_port
        self.command_splitter = command_splitter

        self.methods: "dict[str, MethodType]" = {
            ControlParam.CLAW: self.control_claw,
            ControlParam.EXTEND_ARROW: self.control_extend_arrow,
            ControlParam.RAISE_ARROW: self.control_raise_arrow,
            ControlParam.ROTATION: self.control_rotation,
            ControlParam.LED: self.set_led_rgb,
        }

    def control_claw(self, angle: int) -> None:
        log.info("Set claw angle to %s", angle)
        self.robohand.control_claw(angle)

    def control_extend_arrow(self, angle: int) -> None:
        log.info("Extend tower to angle %s", angle)
        self.robohand.control_extend_arrow(angle)

    def control_raise_arrow(self, angle: int) -> None:
        log.info("Raise tower to angle %s", angle)
        self.robohand.control_raise_arrow(angle)

    def control_rotation(self, angle: int) -> None:
        log.info("Rotate base to angle %s", angle)
        self.robohand.control_rotation(angle)

    def set_led_rgb(self, red: int, green: int, blue: int) -> None:
        log.info("Set led rgb to %s, %s, %s", red, green, blue)
        self.robohand.set_led_rgb(red, green, blue)

    def handle_command(self, command: str) -> None:
        commands = command.split(COMMAND_ENDL)
        for cmd in commands:
            if not cmd:
                continue
            prefix, *args = cmd.split(self.command_splitter)
            if prefix not in self.methods:
                log.warning(
                    "Unknown command prefix %r, cmd %r, full: %r",
                    prefix,
                    cmd,
                    command,
                )
            if prefix not in self.methods:
                log.error(
                    "Error processing command %r, no prefix %r, full command %r.",
                    cmd,
                    prefix,
                    command,
                )
                continue
            method = self.methods[prefix]
            try:
                method(*map(int, args))
            except Exception as e:
                log.error(
                    "Error executing cmd %r command %r: %s. Method: %s",
                    cmd,
                    command,
                    e,
                    method,
                )

    def run_server(self) -> None:
        """
        :return:
        """
        log.debug("Create a TCP socket")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            log.debug("Bind the socket to the server address and port")
            server_socket.bind((SERVER_IP_BIND, SERVER_PORT))
            server_socket.listen()
            # List to keep track of client sockets
            monitor_sockets = [server_socket]

            log.info("Starting server")

            while True:
                # Use select to monitor sockets for incoming data
                readable, _, _ = select.select(monitor_sockets, [], [])

                for sock in readable:
                    if sock is server_socket:
                        # Accept incoming connection
                        client_socket, address = server_socket.accept()
                        log.info("New connection from %s", address)
                        monitor_sockets.append(client_socket)
                    else:
                        # Receive data from the client socket
                        data = sock.recv(1024)
                        if data:
                            d = data.decode()
                            log.debug("Received data %r", d)
                            self.handle_command(d)
                        else:
                            # No new data, close the socket
                            log.info("Client disconnected")
                            monitor_sockets.remove(sock)
                            sock.close()
