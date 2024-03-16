import logging
from typing import TYPE_CHECKING, Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

import config
from app.common.constants import DriveName
from app.common.mappings import NAMES_TO_CONTROL_PARAMS
from app.widgets.debounced_dial import DebouncedDial
from app.widgets.debounced_mirrored_horizontal_slider import (
    DebouncedMirroredHorizontalSlider,
)
from app.widgets.debounced_slider import DebouncedSlider
from app.widgets.lcd_indicator_panel import LcdIndicatorPanel
from robohandcontrol.robocontrol import RobohandControlBase

if TYPE_CHECKING:
    from app.widgets.protocols import RGBValueSettable, ValueSettable


log = logging.getLogger(__name__)


class RoboControlWindow(QWidget):
    def __init__(self, robohand: RobohandControlBase) -> None:
        super().__init__()
        self.robohand: RobohandControlBase = robohand

        self.command_components: "dict[str, ValueSettable | RGBValueSettable]" = {}

        self.indicators_panel = LcdIndicatorPanel(labels=list(DriveName))
        self.control_layout = self.get_robot_control_vertical_layout()
        self.the_main_vertical_layout = QVBoxLayout()
        self.the_main_vertical_layout.addLayout(self.control_layout)

        self.setLayout(self.the_main_vertical_layout)

    def get_claw_control_layout(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        claw_mirrored_slider = DebouncedMirroredHorizontalSlider()
        claw_mirrored_slider.value_changed.connect(
            self.indicators_panel.indicators[DriveName.CLAW].lcd.display,
        )
        claw_mirrored_slider.debounce.add_debounced_handler(self.robohand.control_claw)
        layout.addWidget(claw_mirrored_slider)
        self.command_components[config.ControlParam.CLAW] = claw_mirrored_slider
        return layout

    def get_control_slider_layout(
        self,
        orientation: Qt.Orientation,
        drive_name: DriveName,
        handler: Callable[[int], None],
    ) -> QVBoxLayout:
        layout = QVBoxLayout()
        debounced_slider = DebouncedSlider(orientation=orientation)
        layout.addWidget(debounced_slider)
        debounced_slider.valueChanged.connect(
            self.indicators_panel.indicators[drive_name].lcd.display,
        )
        debounced_slider.add_debounced_handler(handler)

        control_key = NAMES_TO_CONTROL_PARAMS[drive_name]
        self.command_components[control_key] = debounced_slider

        return layout

    def get_extend_control_layout(self) -> QVBoxLayout:
        return self.get_control_slider_layout(
            orientation=Qt.Orientation.Horizontal,
            drive_name=DriveName.EXTEND,
            handler=self.robohand.control_extend_arrow,
        )

    def get_raise_control_layout(self) -> QVBoxLayout:
        return self.get_control_slider_layout(
            orientation=Qt.Orientation.Vertical,
            drive_name=DriveName.RAISE,
            handler=self.robohand.control_raise_arrow,
        )

    def get_rotate_control_layout(self) -> QVBoxLayout:
        layout = QVBoxLayout()

        debounced_dial = DebouncedDial()
        self.command_components[config.ControlParam.ROTATION] = debounced_dial

        debounced_dial.valueChanged.connect(
            self.indicators_panel.indicators[DriveName.ROTATE].lcd.display,
        )
        debounced_dial.add_debounced_handler(self.robohand.control_rotation)

        debounced_dial.setMaximumSize(250, 250)

        layout.addWidget(debounced_dial)
        return layout

    def get_robot_control_vertical_layout(self) -> QVBoxLayout:
        layout = QVBoxLayout()

        claw_control_layout = self.get_claw_control_layout()
        extend_control_layout = self.get_extend_control_layout()
        raise_control_layout = self.get_raise_control_layout()
        rotate_control_layout = self.get_rotate_control_layout()

        h_layout = QHBoxLayout()
        v_layout = QVBoxLayout()

        middle_layout = QHBoxLayout()
        middle_layout.addLayout(rotate_control_layout)
        middle_layout.addWidget(self.indicators_panel)

        layout.addLayout(claw_control_layout)
        v_layout.addLayout(middle_layout)
        h_layout.addLayout(raise_control_layout)
        h_layout.addLayout(v_layout)
        layout.addLayout(extend_control_layout)
        layout.addLayout(h_layout)
        return layout

    def set_state_from_commands(self, commands_text: str) -> None:
        log.info("Run set state from command: %r", commands_text)
        commands = commands_text.split(config.COMMAND_ENDL)
        for command in commands:
            if not command:
                continue
            param, *values = command.split(config.COMMAND_SPLITTER)
            if param not in self.command_components:
                log.warning(
                    "No control component found for key %s, available: %s",
                    param,
                    list(self.command_components),
                )
                continue
            widget = self.command_components[param]
            widget.set_value(*map(int, values))
