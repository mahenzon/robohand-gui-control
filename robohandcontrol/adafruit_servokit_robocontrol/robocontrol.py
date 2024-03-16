"""
https://gist.github.com/mahenzon/203e9d935b42db17c2f57ff69a23b4b0

Example for RoboIntellect RM001 M02 https://t.me/RepkaPitalk/24150
"""

from typing import TYPE_CHECKING

import board
import busio
from adafruit_servokit import ServoKit

from config import DEFAULT_PWM_ADDRESS, LEDPorts, ServoPorts
from robohandcontrol.robocontrol import RobohandControlBase
from robohandcontrol.utils import map_range

if TYPE_CHECKING:
    from adafruit_pca9685 import PCA9685


class RobohandAdafruitServoKitControl(RobohandControlBase):
    def __init__(  # type: ignore
        self,
        sda_pin=board.SDA,  # noqa: ANN001
        scl_pin=board.SCL,  # noqa: ANN001
    ) -> None:
        i2c_bus = busio.I2C(sda_pin, scl_pin)
        self.kit = ServoKit(
            channels=16,
            i2c=i2c_bus,
            address=DEFAULT_PWM_ADDRESS,
        )
        # noinspection PyProtectedMember
        pca: PCA9685 = self.kit._pca

        # I have LED connected to the last three pins on the PCA9685 board
        self.red_channel = pca.channels[LEDPorts.RED_LED_PORT]
        self.green_channel = pca.channels[LEDPorts.GREEN_LED_PORT]
        self.blue_channel = pca.channels[LEDPorts.BLUE_LED_PORT]
        self.led_max_duty_cycle = 0xFFFF

        self.servo_base = self.kit.servo[ServoPorts.SERVO_ROTATE_PORT]
        self.servo_claw = self.kit.servo[ServoPorts.SERVO_CLAW_PORT]
        self.servo_pull = self.kit.servo[ServoPorts.SERVO_ARROW_R_PORT]
        self.servo_raise = self.kit.servo[ServoPorts.SERVO_ARROW_L_PORT]

    def control_claw(self, angle: int) -> None:
        self.servo_claw.angle = angle

    def control_extend_arrow(self, angle: int) -> None:
        self.servo_pull.angle = angle

    def control_raise_arrow(self, angle: int) -> None:
        self.servo_raise.angle = angle

    def control_rotation(self, angle: int) -> None:
        self.servo_base.angle = angle

    def map_color_value(self, value: int) -> int:
        return map_range(
            value,
            in_min=0,
            in_max=255,
            out_min=0,
            out_max=self.led_max_duty_cycle,
        )

    def set_led_rgb(self, red: int, green: int, blue: int) -> None:
        self.red_channel.duty_cycle = self.map_color_value(red)
        self.green_channel.duty_cycle = self.map_color_value(green)
        self.blue_channel.duty_cycle = self.map_color_value(blue)
