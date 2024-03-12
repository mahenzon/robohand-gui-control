from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QLCDNumber, QVBoxLayout, QWidget


class LCDValueIndicatorWidget(QWidget):
    def __init__(
        self,
        label_text: str,
        label_max_height: int = 20,
        lcd_min_height: int = 60,
    ) -> None:
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        label.setMaximumHeight(label_max_height)
        layout.addWidget(label)
        self.lcd = QLCDNumber()
        self.lcd.setMinimumHeight(lcd_min_height)
        layout.addWidget(self.lcd)
        self.setLayout(layout)
