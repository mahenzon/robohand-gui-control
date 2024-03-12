__all__ = ("RobohandControlBase",)

from abc import ABC, abstractmethod


class RobohandControlBase(ABC):
    @abstractmethod
    def control_claw(self, angle: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def control_extend_arrow(self, angle: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def control_raise_arrow(self, angle: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def control_rotation(self, angle: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_led_rgb(self, red: int, green: int, blue: int) -> None:
        raise NotImplementedError
