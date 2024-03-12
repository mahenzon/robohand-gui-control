from typing import Callable

from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtWidgets import QWidget

from app.common.signals import connect_handler_to_signal


class Debounced(QWidget):
    signal = pyqtSignal(int)

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
        connect_handler_to_signal(self.timer.timeout, self.debounced_call)
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
        connect_handler_to_signal(self.signal, handler)
