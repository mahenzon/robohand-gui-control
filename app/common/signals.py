from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable

    from PySide6.QtCore import SignalInstance


def connect_handler_to_signal(
    signal: SignalInstance,
    handler: Callable[[], None] | Callable[[int], None],
) -> None:
    """
    PyCharm doesn't recognise signals as `pyqtBoundSignal`,
    it thinks signals are of type `pyqtSignal`.
    This func handles types for stat-analysis (mypy, etc.).

    :param signal:
    :param handler:
    :return:
    """
    signal.connect(handler)
