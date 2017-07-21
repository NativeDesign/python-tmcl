# -*- coding: UTF-8 -*-
from TMCL.instruction import Instruction
from .tmcl_commands import Command
from .tmcl_axis_parameters import AxisParams


class Motor(object):
	"""
	Motor objects provide an axis-level abstraction layer to a 
	TMCM module connected to a serial bus. You can use it to 
	start & stop movement an individual motor attached to a module,
	configure its axis parameters and initiate reference searches.
	"""

	RFS_START = 0
	RFS_STOP = 1
	RFS_STATUS = 2


	ALLOWED_COMMANDS = [
		Command.ROR,
		Command.ROL,
		Command.MST,
		Command.MVP,
		Command.SAP,
		Command.GAP,
		Command.STAP,
		Command.RSAP,
		Command.RFS,
		Command.SCO,
		Command.GCO,
		Command.CCO
	]


	module = None
	"""
	Module that hosts this motor
	
	:type: TMCL.Module
	"""

	axis = 0
	"""
	Motor axis ID on module
	
	:type:  int
	"""

	def __init__( self, module, axis=0, max_velocity=2047 ):
		"""
		
		:param module: TMCM module instance
		:type  module: TMCL.module.Module
		
		:param axis: Motor axis id
		:type  axis: int
		
		:param max_velocity:
			Maximum valid `velocity_limit` value. Default is 2047, 
			which applies to all known modules except TMCM-100 which 
			should be set to 8191.
		:type max_velocity: int
		"""
		self._max_velocity = max_velocity   # type: int
		self.axis = axis                    # type: int
		self.module = module                # type: TMCL.module.Module


	########################################################################
	#### Core functions
	########################################################################

	def send( self, cmd, type=0, value=0 ):
		"""
		Send a TMCL command to the motor.
		
		Only a subset of TMCL commands are allowed to be sent direct
		to a Motor instance. For more general-purpose TMCL interface,
		use a Module instance.
		
		:param cmd:  
			TMCL command to send to the motor.
			Must be one of ``TMCL.Command.*``
		:type  cmd: int
		
		:param type:  TMCL type parameter 
		:type  type:  int
		
		:param value: TMCL value parameter
		:type  value:  int
		
		:rtype:  TMCL.Reply
		"""
		assert isinstance(cmd,(int,Instruction)),   'cmd must be int or Instruction'
		assert isinstance(type,int),                'type must be an int'
		assert 0 <= type <= 255,                    'type must be in [0..255]'
		assert isinstance(value, int),              'value must be int'

		if isinstance(cmd, Instruction):
			assert cmd.cmd in self.ALLOWED_COMMANDS, 'Specified command cannot target a motor/axis'
			cmd.axis = self.axis
			return self.module.send(cmd)
		else:
			assert cmd in self.ALLOWED_COMMANDS, 'Specified command cannot target a motor/axis'
			return self.module.send(Instruction(cmd, type, self.axis, value))


	def get_axis_param (self, param):
		"""
		Most parameters of a TMCM module can be adjusted individually for 
		each axis. Although these parameters vary widely in their formats 
		(1 to 24 bits, signed or unsigned) and physical locations (TMC428, 
		TMC453, controller RAM, controller EEPROM), they all can be read by 
		this function. In stand-alone mode the requested value is also 
		transferred to the accumulator register for further processing 
		purposes such as conditioned jumps. In direct mode, the value read 
		is only output in the “value” field of the reply, without affecting 
		the accumulator. See chapter 4 for a complete list of all parameters.
		
		:param param: Axis parameter id (see AxisParams)
		:type  param: int
		
		:return: Axis param value. Type depends on param
		:rtype:  int
		"""
		assert isinstance(param, int),  'param must be an int'
		assert 0 <= param <= 255,       'param must be in [0..255]'

		return self.send(Command.GAP, type=param).value


	def set_axis_param (self, param, value):
		"""
		Set an axis parameter on this motor
		
		From the TMCL docs:
			
			Most parameters of a TMCM module can be adjusted individually for 
			each axis. Although these parameters vary widely in their formats 
			(1 to 24 bits, signed or unsigned) and physical locations 
			(TMC428, TMC453, controller RAM, controller EEPROM), they all can 
			be set by this function. See chapter 4 for a complete list of all 
			axis parameters. See STAP (section 3.7) for permanent storage of a 
			modified value.
		
		:param param: Axis parameter id
		:type  param: int
		
		:param value: Value to set
		:type  value: int 
		
		:rtype:  TMCL.Reply
		"""
		assert isinstance(param, int),          'param must be an int'
		assert 0 <= param <= 255,               'param must be in [0..255]'
		assert isinstance(value, (int,long)),   'value must be an int'

		return self.send(Command.SAP, type=param, value=value)


	########################################################################
	#### Utility functions
	########################################################################

	def stop( self ):
		"""
		This instruction stops the motor. 
		
		:rtype: TMCL.Reply
		"""
		return self.send(Command.MST)


	def rotate_left (self, velocity ):
		"""
		This instruction starts rotation in "left" direction, 
		i.e. decreasing the position counter.
		
		:param velocity: Movement velocity
		:type  velocity: int [0..self._max_velocity]
		
		:return: Response status (TMCL.Reply.Status.*)
		:rtype:  int
		"""
		assert isinstance(velocity,int),         'velocity must be an int'
		assert 0 <= velocity <= self._max_velocity,     'velocity must be in [0..'+str(self._max_velocity)+']'

		reply = self.send(Command.ROL, value=velocity)
		return reply.status


	def rotate_right(self, velocity):
		"""
		This instruction starts rotation in "right" direction, 
		i.e. increasing the position counter
		
		:param velocity: Movement velocity
		:type  velocity: int [0..self._max_velocity]
		
		:return: Response status (TMCL.Reply.Status.*)
		:rtype:  int
		"""
		assert isinstance(velocity, int)
		assert 0 <= velocity <= self._max_velocity,     'velocity must be in [0..'+str(self._max_velocity)+']'

		reply = self.send(Command.ROR, value=velocity)
		return reply.status


	def move_absolute (self, position):
		"""
		A movement towards the specified position is started, with 
		automatic generation of acceleration and deceleration ramps. 
		
		The maximum velocity and acceleration are defined by axis 
		parameters MAX_POSITIONING_SPEED and MAX_ACCELERATION.
		
		Moving to an absolute position in the range [±2^23]. 
		
		:param position:  Absolute step position to move to
		:type  position:  int [±2^23]
		:return: 
		"""
		assert isinstance(position, int),   'position must be an int'
		assert -2**23 <= position <= 2**23, 'position must be in range +-2^23'

		reply = self.send(Command.MVP, type=0, value=position)
		return reply.status


	def move_relative (self, offset):
		"""
		A movement towards the specified position is started, with 
		automatic generation of acceleration and deceleration ramps. 
		
		The maximum velocity and acceleration are defined by axis 
		parameters MAX_POSITIONING_SPEED and MAX_ACCELERATION.
		
		Starting a relative movement by means of an offset to the actual position. 
		In this case, the resulting new position value must not exceed ±2^23. 
		
		:param offset: Steps to move relative to current position
		:type  offset: int [±2^23]
		:return: 
		"""
		assert isinstance(offset, int),     'offset must be an int'
		assert -2**23 <= offset <= 2**23,   'Position must be within range +-2^23'

		reply = self.send(Command.MVP, type=1, value=offset)
		return reply.status


	def reference_search( self, rfs_type ):
		"""
		Initiate a reference search.
		
		From the TMCL docs:
		
			A build-in reference point search algorithm can be started (and stopped). 
			The reference search algorithm provides switching point calibration and 
			three switch modes. The status of the reference search can also be queried 
			to see if it has already finished. (In a TMCL program it is better to use 
			the WAIT command to wait for the end of a reference search.) Please see the 
			appropriate parameters in the axis parameter table to configure the reference 
			search algorithm to meet your needs (chapter 4). The reference search can be 
			started or stopped, or the actual status of the reference search can be checked.
		
		:param rfs_type: ``RFS_START | RFS_STOP | RFS_STATUS``
		:type  rfs_type: int
		
		:return: When `rfs_type` == ``RFS_STATUS``; nonzero means reference search in progress
		:rtype:  int
		"""
		assert rfs_type in [
			self.RFS_START,
			self.RFS_STATUS,
			self.RFS_STOP
		], 'rfs_type must be RFS_START | RFS_STATUS | RFS_STOP'

		reply = self.send(Command.RFS, type=rfs_type)
		return reply.status



	########################################################################
	#### Axis parameter helpers
	########################################################################

	@property
	def target_position ( self ):
		"""
		The desired position in position mode.
		
		:type: int 
		"""
		return self.get_axis_param(AxisParams.TARGET_POSITION)


	@target_position.setter
	def target_position ( self, value ):
		self.set_axis_param(AxisParams.TARGET_POSITION, value)


	@property
	def actual_position ( self ):
		"""
		The current position of the motor. Should only be overwritten 
		for reference point setting.
		
		:type: int
		:access: readonly
		"""
		return self.get_axis_param(AxisParams.ACTUAL_POSITION)


	@actual_position.setter
	def actual_position ( self, value ):
		self.set_axis_param(AxisParams.ACTUAL_POSITION, value)


	@property
	def target_speed ( self ):
		"""
		The desired speed in velocity mode (see ramp mode, no. 138). 
		In position mode, this parameter is set by hardware: to the 
		maximum speed during acceleration, and to zero during 
		deceleration and rest.
		
		:type: int 
		"""
		return self.get_axis_param(AxisParams.TARGET_SPEED)


	@target_speed.setter
	def target_speed ( self, value ):
		self.set_axis_param(AxisParams.TARGET_SPEED, value)


	@property
	def actual_speed ( self ):
		"""
		The current rotation speed. Should never be overwritten.
		
		:type: int
		:access: readonly
		"""
		return self.get_axis_param(AxisParams.ACTUAL_SPEED)


	@property
	def max_positioning_speed ( self ):
		"""
		Should not exceed the physically highest possible value.
		Adjust the pulse divisor (no. 154), if the speed value is
		very low (<50) or above the upper limit. See TMC 428
		datasheet (p.24) for calculation of physical units.
		
		:type: int 
		"""
		return self.get_axis_param(AxisParams.MAX_POSITIONING_SPEED)


	@max_positioning_speed.setter
	def max_positioning_speed ( self, value ):
		self.set_axis_param(AxisParams.MAX_POSITIONING_SPEED, value)


	@property
	def max_accelleration ( self ):
		"""
		The limit for acceleration (and deceleration). Changing
		this parameter requires re-calculation of the acceleration
		factor (no. 146) and the acceleration divisor (no.137),
		which is done automatically. See TMC 428 datasheet
		(p.24) for calculation of physical units.
		
		:type: int 
		"""
		return self.get_axis_param(AxisParams.MAX_ACCELLERATION)


	@max_accelleration.setter
	def max_accelleration ( self, value ):
		self.set_axis_param(AxisParams.MAX_ACCELLERATION, value)


	@property
	def max_current ( self ):
		"""
		The most important motor setting, since too high values
		might cause motor damage! Note that on the TMCM-300
		the phase current can not be reduced down to zero due
		to the Allegro A3972 driver hardware.
		On the TMCM-300, 303, 310, 110, 610, 611 and 612 the
		maximum value is 1500 (which means 1.5A).
		On all other modules the maximum value is 255 (which
		means 100% of the maximum current of the module)
		
		:type: int 
		"""
		return self.get_axis_param(AxisParams.MAX_CURRENT)


	@max_current.setter
	def max_current ( self, value ):
		self.set_axis_param(AxisParams.MAX_CURRENT, value)


	@property
	def standby_current ( self ):
		"""
		The current limit two seconds after the motor has stopped.
		The value range of this parameter is the same as with
		parameter 6.
		
		:type: int 
		"""
		return self.get_axis_param(AxisParams.STANDBY_CURRENT)


	@standby_current.setter
	def standby_current ( self, value ):
		self.set_axis_param(AxisParams.STANDBY_CURRENT, value)


	@property
	def target_position_reached ( self ):
		"""
		Indicates that the actual position equals the target position.
		
		:type: int 
		"""
		return self.get_axis_param(AxisParams.TARGET_POSITION_REACHED)


	@property
	def ref_switch_status ( self ):
		"""
		The logical state of the reference (left) switch.
		See the TMC 428 data sheet for the different switch
		modes. Default is two switch mode: the left switch as
		the reference switch, the right switch as a limit (stop)
		switch.
		
		:type: int 
		"""
		return self.get_axis_param(AxisParams.REF_SWITCH_STATUS)


	@property
	def right_limit_status ( self ):
		"""
		The logical state of the (right) limit switch.
		
		:type: int 
		"""
		return self.get_axis_param(AxisParams.RIGHT_LIMIT_SWITCH_STATUS)


	@property
	def left_limit_status ( self ):
		"""
		The logical state of the left limit switch (in three switch mode)
		
		:type: int 
		"""
		return self.get_axis_param(AxisParams.LEFT_LIMIT_SWITCH_STATUS)


	@property
	def right_limit_switch_disabled ( self ):
		"""
		If set, deactivates the stop function of the right switch 
		
		:type: int 
		"""
		return True if self.get_axis_param(AxisParams.RIGHT_LIMIT_SWITCH_DISABLE) == 1 else False


	@right_limit_switch_disabled.setter
	def right_limit_switch_disabled ( self, value ):
		self.set_axis_param(AxisParams.RIGHT_LIMIT_SWITCH_DISABLE, 1 if value else 0)


	@property
	def left_limit_switch_disabled ( self ):
		"""
		Deactivates the stop function of the left switch resp. 
		reference switch if set.
		
		:type: int 
		"""
		return True if self.get_axis_param(AxisParams.LEFT_LIMIT_SWITCH_DISABLE) == 1 else False


	@left_limit_switch_disabled.setter
	def left_limit_switch_disabled ( self, value ):
		self.set_axis_param(AxisParams.LEFT_LIMIT_SWITCH_DISABLE, 1 if value else 0)
