import logging
import sys

from PySide6.QtWidgets import (
    QApplication,
)

import config
from app.common.robohand_getter import robohand_control
from app.widgets.combined_robocontrol_window import CombinedRoboControlWindow


def get_main_window() -> CombinedRoboControlWindow:
    robohand = robohand_control()
    window = CombinedRoboControlWindow(
        robohand,
        store_commands_filename=config.STORE_COMMANDS,
    )
    return window


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)

    window = get_main_window()
    window.show()

    app.exec()
