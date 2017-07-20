from .bus import Bus
from .motor import Motor
from .tmcl_commands import Command
from .reply import Reply
from .tmcl_axis_parameters import AxisParams
from .tmcl_global_parameters import GlobalParams

def connect ( serial_port, CAN = False ):
    return Bus(serial_port, CAN)
