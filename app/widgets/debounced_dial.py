from typing import Callable

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDial

from app.widgets.debounced import Debounced
from robohandcontrol.constants import SERVO_MAX_ANGLE, SERVO_MIN_ANGLE


class DebouncedDial(QDial):
    changed = Signal(int)

    def __init__(
        self,
        notches_visible: bool = True,
        wrapping: bool = False,
        min_value: int = SERVO_MIN_ANGLE,
        max_value: int = SERVO_MAX_ANGLE,
    ) -> None:
        super().__init__()
        self.setNotchesVisible(notches_visible)
        self.setWrapping(wrapping)
        self.setRange(min_value, max_value)

        self.debounce = Debounced()

        self.valueChanged.connect(self.debounce.handle)

    def add_debounced_handler(self, handler: Callable[[int], None]) -> None:
        """
        Your callback handler

        :param handler:
        :return:
        """
        self.debounce.signal.connect(handler)
