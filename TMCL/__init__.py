from .bus import Bus
from .motor import Motor
from .commands import Command
from .reply import Reply

def connect ( serial_port, CAN = False ):
    return Bus(serial_port, CAN)
