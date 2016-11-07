
from .commands import Command


class Motor (object):


    def __init__ (self, bus, address, motor = 0):
        self.bus = bus
        self.address = address
        self.motor = motor
        self.axis = AxisParameterInterface(self)


    def send (self, cmd, type, motorbank, value):
        self.bus.send(self.address, cmd, type, motorbank, value)

    def stop (self):
        self.send( Command.MST, 0, self.motor, 0 )

    def get_user_var (self, n ):
        reply = self.send( Command.GGP, n, 2, 0)
        return reply.value

    def set_user_var (self, n ,value):
        reply = self.send( Command.SGP, n, 2, value )
        return reply.status

    def run_command (self, cmdIndex):
        reply = self.send( Command.RUN_APPLICATION, 1, self.motor, cmdIndex )
        return reply.status








class AxisParameterInterface (object):
    def __init__(self, motor):
        self.motor = motor

    def get (self, param):
        reply = self.motor.send( Command.GAP, param, self.motor.motor, 0)
        return reply.value

    def set (self, param, value):
        reply = self.motor.send( Command.SAP, param, self.motor.motor, value)
        return reply.status


    @property
    def target_position (self):
        return self.get(0)

    @target_position.setter
    def target_position (self, value):
        return self.set(0, value)

    @property
    def actual_position (self):
        return self.get(1)

    @actual_position.setter
    def actual_position (self, value):
        return self.set(1, value)

    @property
    def target_speed (self):
        return self.get(2)

    @target_speed.setter
    def target_speed(self, value):
        return self.set( 2, value )

    @property
    def actual_speed (self):
        return self.get(3)

    @property
    def max_positioning_speed (self):
        return self.get(4)

    @max_positioning_speed.setter
    def max_positioning_speed (self, value):
        return self.set(4, value)

    @property
    def max_accelleration (self):
        return self.get(5)

    @max_accelleration.setter
    def max_accelleration (self, value):
        return self.set( 5, value)

    @property
    def max_current (self):
        return self.get(6)

    @max_current.setter
    def max_current (self, value):
        return self.set(6, value)

    @property
    def standby_current (self):
        return self.get(7)

    @standby_current.setter
    def standby_current (self, value):
        return self.set(7,value)

    @property
    def target_position_reached (self):
        return self.get(8)

    @property
    def ref_switch_status (self):
        return self.get(9)

    @property
    def right_limit_status (self):
        return self.get(10)

    @property
    def left_limit_status (self):
        return self.get(11)

    @property
    def right_limit_switch_disabled (self):
        return True if self.get(12) == 1 else False

    @right_limit_switch_disabled.setter
    def right_limit_switch_disabled (self, value):
        return self.set(12, 1 if value else 0)

    @property
    def left_limit_switch_disabled (self):
        return True if self.get(13) == 1 else False

    @left_limit_switch_disabled.setter
    def left_limit_switch_disabled (self, value):
        return self.set(13, 1 if value else 0)
