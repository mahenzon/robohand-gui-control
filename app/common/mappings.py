import config
from app.common.constants import DriveName

NAMES_TO_CONTROL_PARAMS: "dict[str, str]" = {
    DriveName.ROTATE: config.ControlParam.ROTATION,
    DriveName.RAISE: config.ControlParam.RAISE_ARROW,
    DriveName.EXTEND: config.ControlParam.EXTEND_ARROW,
    DriveName.CLAW: config.ControlParam.CLAW,
}
