from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QSlider

from app.widgets.debounced import Debounced
from app.widgets.mirrored_horizontal_slider import MirroredHorizontalSlider


class DebouncedMirroredHorizontalSlider(MirroredHorizontalSlider):
    value_changed = pyqtSignal(int)

    def __init__(
        self,
        slider_minimum: int = -90,
        slider_maximum: int = 90,
        debounce_time: int = 100,
    ) -> None:
        super().__init__(slider_minimum, slider_maximum)
        self.debounce_time = debounce_time
        self.debounce = Debounced(debounce_time=debounce_time)

    def slider_value_changed(self, dependant: QSlider, value: int) -> None:
        # mirror slider
        mirrored_value = self.slider_maximum + self.slider_minimum - value
        dependant.setValue(mirrored_value)

        # what should be set
        new_value = value if dependant is self.slider_right else mirrored_value
        # debounced signal
        self.debounce.handle(new_value)
        # instant signal
        # noinspection PyUnresolvedReferences
        self.value_changed.emit(new_value)
