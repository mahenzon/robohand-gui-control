import logging
import sys

from PySide6.QtWidgets import (
    QApplication,
)

from app.widgets.robocontrol import RoboControlWindow
from app.common.robohand_getter import robohand_control


def get_main_window() -> RoboControlWindow:
    robohand = robohand_control()
    window = RoboControlWindow(robohand)
    return window


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)

    window = get_main_window()
    window.show()

    app.exec()
