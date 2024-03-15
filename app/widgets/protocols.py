from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Protocol

    class ValueSettable(Protocol):
        def set_value(self, *values: int):
            pass
