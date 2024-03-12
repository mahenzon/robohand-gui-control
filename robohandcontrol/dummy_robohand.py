import logging

from robohandcontrol.robocontrol import RobohandControlBase

log = logging.getLogger(__name__)


class LoggedRobohandControl(RobohandControlBase):
    def __init__(self) -> None:
        log.warning(
            "Starting in logged mode. To run in ri-sdk mode use `--ri-sdk-mode` flag "
            "and to start in adafruit servokit mode use `--adafruit-servokit-mode` flag",
        )

    def control_claw(self, angle: int) -> None:
        log.info("Set claw angle to %s", angle)

    def control_extend_arrow(self, angle: int) -> None:
        log.info("Extend tower to angle %s", angle)

    def control_raise_arrow(self, angle: int) -> None:
        log.info("Raise tower to angle %s", angle)

    def control_rotation(self, angle: int) -> None:
        log.info("Rotate base to angle %s", angle)

    def set_led_rgb(self, red: int, green: int, blue: int) -> None:
        log.info("Set led rgb to %s, %s, %s", red, green, blue)
