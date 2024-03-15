from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Protocol

    class ValueSettable(Protocol):
        def set_value(self, value: int) -> None:
            pass

    class RGBValueSettable(Protocol):
        def set_value(self, red: int, green: int, blue: int) -> None:
            pass
