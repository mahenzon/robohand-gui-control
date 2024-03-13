from collections.abc import Iterable

from PySide6.QtWidgets import QHBoxLayout, QWidget

from app.widgets.lcd_value_indicator_widget import LCDValueIndicatorWidget


class LcdIndicatorPanel(QWidget):
    def __init__(self, labels: Iterable[str]) -> None:
        super().__init__()

        horizontal_layout = QHBoxLayout()

        indicators = {}
        for label_text in labels:
            indicator = LCDValueIndicatorWidget(label_text)
            indicators[label_text] = indicator
            horizontal_layout.addWidget(indicator)

        self.indicators = indicators
        self.setLayout(horizontal_layout)
