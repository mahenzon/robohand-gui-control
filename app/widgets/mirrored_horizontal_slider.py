from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QSlider, QWidget

from app.common.signals import connect_handler_to_signal
from robohandcontrol.constants import SERVO_MAX_ANGLE, SERVO_MIN_ANGLE


class MirroredHorizontalSlider(QWidget):
    def __init__(
        self,
        slider_minimum: int = SERVO_MIN_ANGLE,
        slider_maximum: int = SERVO_MAX_ANGLE,
    ) -> None:
        super().__init__()

        self.slider_minimum = slider_minimum
        self.slider_maximum = slider_maximum

        h_layout = QHBoxLayout()

        self.slider_left = self.init_slider(self.left_slider_changed)
        self.slider_right = self.init_slider(self.right_slider_changed)

        h_layout.addWidget(self.slider_left)
        h_layout.addWidget(self.slider_right)
        self.slider_left.setValue((self.slider_maximum + self.slider_minimum) // 2)

        self.setLayout(h_layout)

    def init_slider(self, handler: Callable[[int], None]) -> QSlider:
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(self.slider_minimum)
        slider.setMaximum(self.slider_maximum)
        slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        connect_handler_to_signal(slider.valueChanged, handler=handler)
        return slider

    def left_slider_changed(self, value: int) -> None:
        self.slider_value_changed(self.slider_right, value)

    def right_slider_changed(self, value: int) -> None:
        self.slider_value_changed(self.slider_left, value)

    def slider_value_changed(self, dependant: QSlider, value: int) -> None:
        # mirror slider
        mirrored_value = self.slider_maximum + self.slider_minimum - value
        dependant.setValue(mirrored_value)
