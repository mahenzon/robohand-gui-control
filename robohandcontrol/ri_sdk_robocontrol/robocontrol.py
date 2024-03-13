from ri_sdk import contrib

from robohandcontrol.ri_sdk_robocontrol.ri_sdk_robohand_wrapper import (
    RoboHand,
    ServoInfo,
)
from robohandcontrol.robocontrol import RobohandControlBase


class RobohandRISDKControl(RobohandControlBase):
    def __init__(self, robohand: RoboHand) -> None:
        self.robohand = robohand
        self.speed = 50

    def set_servo_angle(self, servo: ServoInfo, angle: int) -> None:
        self.robohand.turn_servo(
            servo.descriptor,
            angle=angle,
            speed=self.speed,
        )

    def control_claw(self, angle: int) -> None:
        self.set_servo_angle(self.robohand.servo_claw, angle)

    def control_extend_arrow(self, angle: int) -> None:
        self.set_servo_angle(self.robohand.servo_pull, angle)

    def control_raise_arrow(self, angle: int) -> None:
        self.set_servo_angle(self.robohand.servo_raise, angle)

    def control_rotation(self, angle: int) -> None:
        self.set_servo_angle(self.robohand.servo_rotate, angle)

    def set_led_rgb(self, red: int, green: int, blue: int) -> None:
        self.robohand.set_led(
            red=red,
            green=green,
            blue=blue,
        )


def get_ri_sdk_control() -> RobohandRISDKControl:
    lib = contrib.get_lib()
    robohand = RoboHand(lib)
    robohand.init_servos()
    robohand.servos_to_start_position()
    return RobohandRISDKControl(robohand)
