from typing import Callable, cast

from PyQt6.QtCore import pyqtSignal, pyqtBoundSignal


def connect_handler_to_signal(signal: pyqtSignal, handler: Callable) -> None:
    signal_ = cast(pyqtBoundSignal, signal)
    signal_.connect(handler)
