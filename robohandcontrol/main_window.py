import logging
import sys

from PySide6.QtWidgets import (
    QApplication,
)

from app.common.robohand_getter import robohand_control
from app.widgets.combined_robocontrol_window import CombinedRoboControlWindow


def get_main_window() -> CombinedRoboControlWindow:
    robohand = robohand_control()
    window = CombinedRoboControlWindow(robohand)
    return window


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)

    window = get_main_window()
    window.show()

    app.exec()
