from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QSlider

from app.widgets.debounced import Debounced
from app.widgets.mirrored_horizontal_slider import MirroredHorizontalSlider
from robohandcontrol.constants import SERVO_MAX_ANGLE, SERVO_MIN_ANGLE


class DebouncedMirroredHorizontalSlider(MirroredHorizontalSlider):
    value_changed = pyqtSignal(int)

    def __init__(
        self,
        slider_minimum: int = SERVO_MIN_ANGLE,
        slider_maximum: int = SERVO_MAX_ANGLE,
        debounce_time: int = 1500,
    ) -> None:
        self.debounce_time = debounce_time
        self.debounce = Debounced(debounce_time=debounce_time)
        self.debounce.add_debounced_handler(self.debounced_update)
        super().__init__(slider_minimum, slider_maximum)
        self.slider_left.setDisabled(True)

    def slider_value_changed(self, dependant: QSlider, value: int) -> None:
        self.slider_right.blockSignals(True)
        self.slider_left.blockSignals(True)

        # mirror slider
        mirrored_value = self.slider_maximum + self.slider_minimum - value
        dependant.setValue(mirrored_value)

        # what should be set
        new_value = value if dependant is self.slider_left else mirrored_value
        # debounced signal
        self.debounce.handle(new_value)
        # instant signal
        # noinspection PyUnresolvedReferences
        self.value_changed.emit(new_value)

        self.slider_right.blockSignals(False)
        self.slider_left.blockSignals(False)

    def debounced_update(self, value: int) -> None:
        self.slider_right.blockSignals(True)
        self.slider_left.blockSignals(True)

        mirrored_value = self.slider_maximum + self.slider_minimum - value
        self.slider_right.setValue(mirrored_value)
        self.slider_left.setValue(value)

        self.slider_right.blockSignals(False)
        self.slider_left.blockSignals(False)
