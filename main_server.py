import logging

from robohandcontrol.common import robohand_control
from robohandcontrol.server_socket_robocontrol.robocontrol import (
    RobohandControlServerSocket,
)


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    control = RobohandControlServerSocket(
        robohand=robohand_control(),
    )
    control.run_server()


if __name__ == "__main__":
    main()
