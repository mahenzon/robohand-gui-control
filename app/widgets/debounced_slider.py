from typing import Callable

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import QSlider

from app.common.signals import connect_handler_to_signal
from app.styles.slider import SLIDER_STYLESHEET_BIG_HANDLE


class DebouncedSlider(QSlider):
    changed = pyqtSignal(int)

    def __init__(
        self,
        orientation: Qt.Orientation,
        slider_minimum: int = -90,
        slider_maximum: int = 90,
        debounce_time: int = 100,
    ) -> None:
        """
        :param slider_minimum:
        :param slider_maximum:
        :param debounce_time: in milliseconds
        """
        super().__init__()
        self.timer = QTimer()
        self.timer.setInterval(debounce_time)
        self.timer.setSingleShot(True)
        connect_handler_to_signal(self.timer.timeout, self.debounced_call)
        # slider
        self.setOrientation(orientation)
        self.setMinimum(slider_minimum)
        self.setMaximum(slider_maximum)
        connect_handler_to_signal(self.valueChanged, self.slider_changed)

        self.setStyleSheet(SLIDER_STYLESHEET_BIG_HANDLE)

    def debounced_call(self) -> None:
        # noinspection PyUnresolvedReferences
        self.changed.emit(self.value())

    def slider_changed(self) -> None:
        # Starts or restarts the timer with the timeout specified in interval.
        self.timer.start()

    def add_debounced_handler(self, handler: Callable[[int], None]) -> None:
        """
        Your callback handler

        :param handler:
        :return:
        """
        connect_handler_to_signal(self.changed, handler)
