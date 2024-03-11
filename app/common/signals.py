from typing import Callable, TypeVar, Union

from PyQt6.QtCore import pyqtBoundSignal, pyqtSignal

SignalType = TypeVar("SignalType", bound=Union[pyqtSignal, pyqtBoundSignal])


def connect_handler_to_signal(
    signal: SignalType,
    handler: Callable[[int], None],
) -> None:
    """
    PyCharm doesn't recognise signals as `pyqtBoundSignal`,
    it thinks signals are of type `pyqtSignal`.
    This func handles types for stat-analysis (mypy, etc.).

    :param signal:
    :param handler:
    :return:
    """
    if isinstance(signal, pyqtBoundSignal):
        signal.connect(handler)

    msg = f"Signal must be of type `pyqtBoundSignal`, got {type(signal)}"
    raise TypeError(msg)
