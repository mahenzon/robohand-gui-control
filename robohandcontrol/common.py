import sys
from typing import TYPE_CHECKING

from robohandcontrol.dummy_robohand import LoggedRobohandControl

if TYPE_CHECKING:
    from robohandcontrol.adafruit_servokit_robocontrol.robocontrol import (
        RobohandAdafruitServoKitControl,
    )
    from robohandcontrol.client_socket_robocontrol.robocontrol import (
        RobohandControlClientSocket,
    )
    from robohandcontrol.ri_sdk_robocontrol.robocontrol import RobohandRISDKControl
    from robohandcontrol.robocontrol import RobohandControlBase


def get_robohand_for_ri_sdk() -> "RobohandRISDKControl":
    from robohandcontrol.ri_sdk_robocontrol.robocontrol import get_ri_sdk_control

    return get_ri_sdk_control()


def get_robohand_for_adafruit_servokit() -> "RobohandAdafruitServoKitControl":
    from robohandcontrol.adafruit_servokit_robocontrol.robocontrol import (
        RobohandAdafruitServoKitControl,
    )

    return RobohandAdafruitServoKitControl()


def get_robohand_socket_client_mode() -> "RobohandControlClientSocket":
    import config
    from robohandcontrol.client_socket_robocontrol.robocontrol import (
        RobohandControlClientSocket,
    )

    return RobohandControlClientSocket(
        server_host=config.SERVER_IP_CONNECT,
        server_port=config.SERVER_PORT,
        command_splitter=config.COMMAND_SPLITTER,
    )


def robohand_control() -> "RobohandControlBase":
    run_sdk_mode = "--ri-sdk-mode" in sys.argv
    run_adafruit_servokit_mode = "--adafruit-servokit-mode" in sys.argv
    socket_client_mode = "--socket-client-mode" in sys.argv
    if (run_sdk_mode + run_adafruit_servokit_mode + socket_client_mode) > 1:
        msg = (
            "You cannot run more than one of "
            "`--ri-sdk-mode` / `--adafruit-servokit-mode` / `--socket-client-mode`"
            ". Please choose either one"
        )
        raise ValueError(msg)
    if run_sdk_mode:
        return get_robohand_for_ri_sdk()
    if run_adafruit_servokit_mode:
        return get_robohand_for_adafruit_servokit()
    if socket_client_mode:
        return get_robohand_socket_client_mode()
    return LoggedRobohandControl()
