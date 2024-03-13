import logging
import sys
from enum import Enum
from typing import TYPE_CHECKING, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

from app.common.signals import connect_handler_to_signal
from app.widgets.debounced_dial import DebouncedDial
from app.widgets.debounced_mirrored_horizontal_slider import (
    DebouncedMirroredHorizontalSlider,
)
from app.widgets.debounced_slider import DebouncedSlider
from app.widgets.lcd_indicator_panel import LcdIndicatorPanel
from robohandcontrol.dummy_robohand import LoggedRobohandControl
from robohandcontrol.robocontrol import RobohandControlBase

if TYPE_CHECKING:
    from robohandcontrol.adafruit_servokit_robocontrol.robocontrol import (
        RobohandAdafruitServoKitControl,
    )
    from robohandcontrol.ri_sdk_robocontrol.robocontrol import RobohandRISDKControl


class DriveName(str, Enum):
    ROTATE = "Rotate"
    RAISE = "Raise"
    EXTEND = "Extend"
    CLAW = "Claw"


class MainWindow(QWidget):
    def __init__(self, robohand: RobohandControlBase) -> None:
        super().__init__()
        self.robohand: RobohandControlBase = robohand

        self.indicators_panel = LcdIndicatorPanel(labels=list(DriveName))
        self.the_main_vertical_layout = QVBoxLayout()
        control_layout = self.get_robot_control_vertical_layout()
        self.the_main_vertical_layout.addLayout(control_layout)

        self.setLayout(self.the_main_vertical_layout)
        self.setWindowTitle("RI RoboHand Control")
        self.setGeometry(300, 200, 900, 500)

    def get_claw_control_layout(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        claw_mirrored_slider = DebouncedMirroredHorizontalSlider()
        connect_handler_to_signal(
            claw_mirrored_slider.value_changed,
            self.indicators_panel.indicators[DriveName.CLAW].lcd.display,
        )
        claw_mirrored_slider.debounce.add_debounced_handler(self.robohand.control_claw)
        layout.addWidget(claw_mirrored_slider)
        return layout

    def get_control_slider_layout(
        self,
        orientation: Qt.Orientation,
        drive_name: DriveName,
        handler: "Callable[[int], None]",
    ) -> QVBoxLayout:
        layout = QVBoxLayout()
        debounced_slider = DebouncedSlider(orientation=orientation)
        layout.addWidget(debounced_slider)
        connect_handler_to_signal(
            debounced_slider.valueChanged,
            self.indicators_panel.indicators[drive_name].lcd.display,
        )
        debounced_slider.add_debounced_handler(handler)
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

        connect_handler_to_signal(
            debounced_dial.valueChanged,
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


def get_robohand_for_ri_sdk() -> "RobohandRISDKControl":
    from robohandcontrol.ri_sdk_robocontrol.robocontrol import get_ri_sdk_control

    return get_ri_sdk_control()


def get_robohand_for_adafruit_servokit() -> "RobohandAdafruitServoKitControl":
    from robohandcontrol.adafruit_servokit_robocontrol.robocontrol import (
        RobohandAdafruitServoKitControl,
    )

    return RobohandAdafruitServoKitControl()


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)

    robohand: RobohandControlBase
    run_sdk_mode = "--ri-sdk-mode" in sys.argv
    run_adafruit_servokit_mode = "--adafruit-servokit-mode" in sys.argv
    if run_sdk_mode and run_adafruit_servokit_mode:
        msg = (
            "You cannot run both --ri-sdk-mode and --adafruit-servokit-mode. "
            "Please choose either one"
        )
        raise ValueError(msg)
    if run_sdk_mode:
        robohand = get_robohand_for_ri_sdk()
    elif run_adafruit_servokit_mode:
        robohand = get_robohand_for_adafruit_servokit()
    else:
        robohand = LoggedRobohandControl()
    window = MainWindow(robohand)
    window.show()

    app.exec()
