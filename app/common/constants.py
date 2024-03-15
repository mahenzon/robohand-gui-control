from enum import Enum


class DriveName(str, Enum):
    ROTATE = "Rotate"
    RAISE = "Raise"
    EXTEND = "Extend"
    CLAW = "Claw"
