import os
from enum import Enum
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SERVER_IP_CONNECT = os.getenv("SERVER_IP_CONNECT", "127.0.0.1")
SERVER_IP_BIND = "0.0.0.0"  # noqa: S104
SERVER_PORT = 61234
CONNECT_TIMEOUT = 1

COMMAND_SPLITTER = "|"
COMMAND_ENDL = ";"

STORE_COMMANDS = "commands.json"

COMMANDS_TIMEOUT = 500


class ControlParam(str, Enum):
    CLAW = "claw"
    EXTEND_ARROW = "extend_arrow"
    RAISE_ARROW = "raise_arrow"
    ROTATION = "rotation"
    LED = "led"


# адрес ШИМ по умолчанию
DEFAULT_PWM_ADDRESS = 0x40


class ServoPorts:
    """
    Порты сервоприводов
    """

    # порт сервопривода тела
    SERVO_ROTATE_PORT = 0
    # порт сервопривода клешни
    SERVO_CLAW_PORT = 1
    # порт сервопривода правой стрелы (выпад вперед)
    SERVO_ARROW_R_PORT = 2
    # порт сервопривода левой стрелы (подъем)
    SERVO_ARROW_L_PORT = 3


class LEDPorts:
    """
    Порты подключения светодиода:
    """

    RED_LED_PORT = 15
    GREEN_LED_PORT = 14
    BLUE_LED_PORT = 13


SERVO_MIN_ANGLE = -85
SERVO_MAX_ANGLE = 85
DEBOUNCE_TIME = 200
