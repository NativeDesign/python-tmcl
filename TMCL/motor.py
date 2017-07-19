# -*- coding: UTF-8 -*-

from .axis_parameters import AxisParameterInterface
from .commands import Command
from .module import Module
from .axis_parameters import AxisParams


class Motor(object, AxisParams):
	"""
	Motor objects provide an axis-level abstraction layer to a 
	TMCM module connected to a serial bus. You can use it to 
	start & stop movement an individual motor attached to a module,
	configure its axis parameters and initiate reference searches.
	"""

	RFS_START = 0
	RFS_STOP = 1
	RFS_STATUS = 2

	def __init__( self, module, axis=0, max_velocity=2047 ):
		"""
		
		:param module: TMCM module object
		:type  module: Module
		
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
		self.module = None                  # type: Module


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
			Must be one of TMCL.Command.* values
		:type  cmd: int
		
		:param type:  TMCL type parameter 
		:type  type:  int
		
		:param value: TMCL value parameter
		:type  type:  int
		
		:rtype:  TMCL.Reply
		"""
		if cmd not in [
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
		]: raise AttributeError("Specified command cannot target a motor/axis")

		return self.module.send( cmd, type, self.axis, value)


	def get_axis_param (self, param):
		"""
		Get the value of an axis parameter
		
		:param param: Axis parameter id (see AxisParams)
		:type  param: int
		
		:return: Axis param value. Type depends on param
		:rtype:  int
		"""
		reply = self.send(Command.GAP, type=param)
		return reply.value


	def set_axis_param (self, param, value):
		"""
		Set an axis param on this motor
		
		:param param: Axis parameter id
		:type  param: int
		
		:param value: Value to set
		:type  value: int 
		
		:rtype:  TMCL.Reply
		"""
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
		if not (0 <= velocity <= self._max_velocity):
			raise ValueError("Velocity must be between 0 and "+str(self._max_velocity))

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
		if not (0 <= velocity <= self._max_velocity):
			raise ValueError("Velocity must be between 0 and "+str(self._max_velocity))

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
		if not ( -2**23 <= position <= 2**23):
			raise ValueError("Position must be within range +-2^23")

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
		if not ( -2**23 <= offset <= 2**23):
			raise ValueError("Position must be within range +-2^23")

		reply = self.send(Command.MVP, type=1, value=offset)
		return reply.status


	# def run_command( self, cmdIndex ):
	# 	"""
	#
	# 	:param cmdIndex:
	# 	:return:
	# 	"""
	# 	reply = self.send(Command.RUN_APPLICATION, 1, self.motor_id, cmdIndex)
	# 	return reply.status


	def reference_search( self, rfs_type ):
		"""
		A build-in reference point search algorithm can be started (and stopped). 
		The reference search algorithm provides switching point calibration and 
		three switch modes. The status of the reference search can also be queried 
		to see if it has already finished. (In a TMCL program it is better to use 
		the WAIT command to wait for the end of a reference search.) Please see the 
		appropriate parameters in the axis parameter table to configure the reference 
		search algorithm to meet your needs (chapter 4). The reference search can be 
		started or stopped, or the actual status of the reference search can be checked.
		
		:param rfs_type: RFS_START | RFS_STOP | RFS_STATUS
		:type  rfs_type: int
		
		:return: When `rfs_type` == RFS_STATUS; nonzero means reference search in progress
		:rtype:  int
		"""
		if not rfs_type in [
			self.RFS_START,
			self.RFS_STATUS,
			self.RFS_STOP
		]: raise ValueError("rfs_type must be RFS_START | RFS_STATUS | RFS_STOP")

		reply = self.send(Command.RFS, type=rfs_type)
		return reply.status



	########################################################################
	#### Axis parameter helpers
	########################################################################

	@property
	def target_position ( self ):
		return self.get_axis_param(AxisParams.TARGET_POSITION)


	@target_position.setter
	def target_position ( self, value ):
		self.set_axis_param(AxisParams.TARGET_POSITION, value)


	@property
	def actual_position ( self ):
		return self.get_axis_param(AxisParams.ACTUAL_POSITION)


	@actual_position.setter
	def actual_position ( self, value ):
		self.set_axis_param(AxisParams.ACTUAL_POSITION, value)


	@property
	def target_speed ( self ):
		return self.get_axis_param(AxisParams.TARGET_SPEED)


	@target_speed.setter
	def target_speed ( self, value ):
		self.set_axis_param(AxisParams.TARGET_SPEED, value)


	@property
	def actual_speed ( self ):
		return self.get_axis_param(AxisParams.ACTUAL_SPEED)


	@property
	def max_positioning_speed ( self ):
		return self.get_axis_param(AxisParams.MAX_POSITIONING_SPEED)


	@max_positioning_speed.setter
	def max_positioning_speed ( self, value ):
		self.set_axis_param(AxisParams.MAX_POSITIONING_SPEED, value)


	@property
	def max_accelleration ( self ):
		return self.get_axis_param(AxisParams.MAX_ACCELLERATION)


	@max_accelleration.setter
	def max_accelleration ( self, value ):
		self.set_axis_param(AxisParams.MAX_ACCELLERATION, value)


	@property
	def max_current ( self ):
		return self.get_axis_param(AxisParams.MAX_CURRENT)


	@max_current.setter
	def max_current ( self, value ):
		self.set_axis_param(AxisParams.MAX_CURRENT, value)


	@property
	def standby_current ( self ):
		return self.get_axis_param(AxisParams.STANDBY_CURRENT)


	@standby_current.setter
	def standby_current ( self, value ):
		self.set_axis_param(AxisParams.STANDBY_CURRENT, value)


	@property
	def target_position_reached ( self ):
		return self.get_axis_param(AxisParams.TARGET_POSITION_REACHED)


	@property
	def ref_switch_status ( self ):
		return self.get_axis_param(AxisParams.REF_SWITCH_STATUS)


	@property
	def right_limit_status ( self ):
		return self.get_axis_param(AxisParams.RIGHT_LIMIT_SWITCH_STATUS)


	@property
	def left_limit_status ( self ):
		return self.get_axis_param(AxisParams.LEFT_LIMIT_SWITCH_STATUS)


	@property
	def right_limit_switch_disabled ( self ):
		return True if self.get_axis_param(AxisParams.RIGHT_LIMIT_SWITCH_DISABLE) == 1 else False


	@right_limit_switch_disabled.setter
	def right_limit_switch_disabled ( self, value ):
		self.set_axis_param(AxisParams.RIGHT_LIMIT_SWITCH_DISABLE, 1 if value else 0)


	@property
	def left_limit_switch_disabled ( self ):
		return True if self.get_axis_param(AxisParams.LEFT_LIMIT_SWITCH_DISABLE) == 1 else False


	@left_limit_switch_disabled.setter
	def left_limit_switch_disabled ( self, value ):
		self.set_axis_param(AxisParams.LEFT_LIMIT_SWITCH_DISABLE, 1 if value else 0)
