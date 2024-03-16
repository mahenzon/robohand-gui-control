import logging
from typing import Callable, Optional

from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QWidget

import config

log = logging.getLogger(__name__)


class DelayedCommandsTimer(QWidget):
    timer_signal = Signal(int)
    timer_finished = Signal()

    def __init__(
        self,
        handler: "Callable[[str], None]",
        timeout: int = config.COMMANDS_TIMEOUT,
    ) -> None:
        super().__init__()
        self.timeout = timeout
        self.handler = handler
        self.index = 0
        self.timer = QTimer()
        self.commands = []
        self.timer_finished.connect(self.reset)
        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.send_command)

    def start(self) -> None:
        log.info("Start commands timer w/ commands %s", self.commands)
        self.timer.start(self.timeout)

    def reset(self, commands: "Optional[list[str]]" = None) -> None:
        self.timer.stop()
        self.index = 0
        self.commands = commands or []

    def send_command(self) -> None:
        self.timer_signal.emit(self.index)
        self.handler(self.commands[self.index])

        self.index += 1

        if self.index >= len(self.commands):
            self.timer.stop()
            self.timer_finished.emit()
