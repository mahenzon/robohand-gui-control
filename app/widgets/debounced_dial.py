from typing import Callable

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QDial

from app.common.signals import connect_handler_to_signal
from app.widgets.debounced import Debounced


class DebouncedDial(QDial):
    changed = pyqtSignal(int)

    def __init__(
        self,
        notches_visible: bool = True,
        wrapping: bool = False,
        min_value: int = -90,
        max_value: int = 90,
    ) -> None:
        super().__init__()
        self.setNotchesVisible(notches_visible)
        self.setWrapping(wrapping)
        self.setRange(min_value, max_value)

        self.debounce = Debounced()

        connect_handler_to_signal(
            self.valueChanged,
            self.debounce.handle,
        )

    def add_debounced_handler(self, handler: Callable[[int], None]) -> None:
        """
        Your callback handler

        :param handler:
        :return:
        """
        connect_handler_to_signal(self.debounce.signal, handler)
