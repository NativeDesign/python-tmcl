from .bus import Bus
from .motor import Motor
from .commands import Command
from .reply import Reply
from .axis_parameters import AxisParams

def connect ( serial_port, CAN = False ):
    return Bus(serial_port, CAN)
