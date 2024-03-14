from typing import Callable

from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QWidget


class Debounced(QWidget):
    signal = Signal(int)

    def __init__(
        self,
        debounce_time: int = 100,
    ) -> None:
        """
        :param debounce_time: in milliseconds
        """
        super().__init__()

        self.timer = QTimer()
        self.timer.setInterval(debounce_time)
        self.timer.setSingleShot(True)
        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.debounced_call)
        self.value = 0

    def debounced_call(self) -> None:
        # (PyCharm typing error)
        # noinspection PyUnresolvedReferences
        self.signal.emit(self.value)

    def handle(self, value: int) -> None:
        self.value = value
        # Starts or restarts the timer with the timeout specified in interval.
        self.timer.start()

    def add_debounced_handler(self, handler: Callable[[int], None]) -> None:
        """
        Your callback handler

        :param handler:
        :return:
        """
        self.signal.connect(handler)
