from typing import Callable

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import QSlider

from app.styles.slider import SLIDER_STYLESHEET_BIG_HANDLE
from config import DEBOUNCE_TIME, SERVO_MAX_ANGLE, SERVO_MIN_ANGLE


class DebouncedSlider(QSlider):
    changed = Signal(int)

    def __init__(
        self,
        orientation: Qt.Orientation,
        slider_minimum: int = SERVO_MIN_ANGLE,
        slider_maximum: int = SERVO_MAX_ANGLE,
        debounce_time: int = DEBOUNCE_TIME,
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
        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.debounced_call)
        # slider
        self.setOrientation(orientation)
        self.setMinimum(slider_minimum)
        self.setMaximum(slider_maximum)
        self.valueChanged.connect(self.slider_changed)

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
        self.changed.connect(handler)

    def set_value(self, value: int) -> None:
        self.setValue(value)
