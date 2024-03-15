import os
from enum import Enum

SERVER_IP_CONNECT = os.getenv("SERVER_IP_CONNECT", "127.0.0.1")
SERVER_IP_BIND = "0.0.0.0"  # noqa: S104
SERVER_PORT = 61234
CONNECT_TIMEOUT = 1

COMMAND_SPLITTER = "|"
COMMAND_ENDL = ";"


class ControlParam(str, Enum):
    CLAW = "claw"
    EXTEND_ARROW = "extend_arrow"
    RAISE_ARROW = "raise_arrow"
    ROTATION = "rotation"
    LED = "led"
