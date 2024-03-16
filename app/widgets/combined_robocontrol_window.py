import logging
import sys

from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtWidgets import QApplication, QHBoxLayout, QSplitter, QWidget

import config
from app.common.mappings import NAMES_TO_CONTROL_PARAMS
from app.common.robohand_getter import robohand_control
from app.widgets.delayed_commands_timer import DelayedCommandsTimer
from app.widgets.robocontol_predefined_commands import (
    RoboControlPredefinedCommandsWidget,
)
from app.widgets.robocontrol import RoboControlWindow
from robohandcontrol.robocontrol import RobohandControlBase


class CombinedRoboControlWindow(QWidget):
    def __init__(
        self,
        robohand: RobohandControlBase,
        store_commands_filename: "str | None" = None,
    ) -> None:
        super().__init__()

        self.robo_control = RoboControlWindow(robohand)

        self.predefined_commands = RoboControlPredefinedCommandsWidget(
            filename=store_commands_filename,
        )
        self.splitter = QSplitter(self)

        self.splitter.addWidget(self.robo_control)
        self.splitter.addWidget(self.predefined_commands)

        self.main_layout = QHBoxLayout()

        self.main_layout.addWidget(self.splitter)
        self.setLayout(self.main_layout)

        self.register_actions()
        self.commands_timer = DelayedCommandsTimer(
            handler=self.robo_control.set_state_from_commands,
        )
        self.commands_timer.timer_finished.connect(
            self.handle_run_commands_finished,
        )

        self.setWindowTitle("RI RoboHand Control")
        self.setGeometry(400, 300, 1200, 600)

    def register_actions(self) -> None:
        self.predefined_commands.add_button.clicked.connect(
            self.handle_save_current_state,
        )
        self.predefined_commands.list_view.doubleClicked.connect(
            self.handle_command_double_clicked,
        )
        self.predefined_commands.run_commands_button.clicked.connect(
            self.handle_run_commands,
        )

    def get_current_state_as_commands_text(self) -> str:
        states = []
        for name, indicator in self.robo_control.indicators_panel.indicators.items():
            value = indicator.lcd.value()
            command = NAMES_TO_CONTROL_PARAMS[name]
            states.append(config.COMMAND_SPLITTER.join((command, str(int(value)))))
        # add endl
        states.append("")
        commands_text = config.COMMAND_ENDL.join(states)
        return commands_text

    def handle_save_current_state(self) -> None:
        commands_text = self.get_current_state_as_commands_text()
        self.predefined_commands.add_element(commands_text)

    def handle_command_double_clicked(self, index: QModelIndex) -> None:
        model = self.predefined_commands.string_list_model
        command_value = model.data(index, Qt.DisplayRole)  # type: ignore[attr-defined]
        self.robo_control.set_state_from_commands(command_value)

    def handle_run_commands_finished(self):
        self.commands_timer.reset()
        self.predefined_commands.set_run_button_icon_play()

    def handle_run_commands(self) -> None:
        if self.commands_timer.timer.isActive():
            self.commands_timer.timer.stop()
            self.handle_run_commands_finished()
        else:
            commands = self.predefined_commands.string_list_model.stringList()
            self.commands_timer.reset(commands=commands)
            self.commands_timer.start()
            self.predefined_commands.set_run_button_icon_stop()


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    app = QApplication(sys.argv)
    robohand = robohand_control()
    main_window = CombinedRoboControlWindow(robohand)
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
