# -*- coding: UTF-8 -*-
from .tmcl_commands import Command
from .motor import Motor


class Module(object):
	"""
	Represents a single TMCM module present on the bus.
	"""


	def __init__ ( self, bus, address=1 ):
		"""        
		:param bus: 
			A Bus instance that is connected to one or more 
			physical TMCM modules via serial port
		:type  bus: TMCL.Bus

		:param address: 
			Module address. This defaults to 1
		:type  address: int

		"""
		assert isinstance(address, int), "Address must be an int"
		assert 0 <= address <= 255,      "Address must be 0 <= address <= 255"

		self.bus = bus
		self.address = address


	########################################################################
	#### Core functions
	########################################################################


	def send (self, cmd, type=0, motbank=0, value=0):
		"""
		Send a TMCL command to the module
		
		:param cmd:  
			TMCL command to send to the motor.
			Must be one of TMCL.Command.* values
		:type  cmd: int
		
		:param type:  TMCL type parameter 
		:type  type:  int
		
		:param motbank: TMCL motor/bank parameter
		:type  motbank: int
		
		:param value: TMCL value parameter
		:type  type:  int
		
		:rtype:  TMCL.Reply
		"""
		return self.bus.send( self.address, cmd, type, motbank, value)


	def get_axis (self, *args, **kwargs):
		"""
		Alias of get_motor
		"""
		return self.get_motor(*args, **kwargs)


	def get_motor ( self, axis=0, max_velocity=None ):
		"""
		Return an interface to a single axis (motor) connected to 
		this module.

		:param axis: 
			Axis ID (defaults to 0)
		:type axis: int
		
		:param max_velocity: 
			Maximum allowed velocity. See Motor for details
		:type  max_velocity: int

		:return: An interface to the desired axis/motor
		:rtype:  Motor
		"""
		return Motor(self, axis=axis, max_velocity=max_velocity)


	def set_axis_param ( self, param, value, axis=0):
		"""
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
		
		:param axis:  Motor axis to set param on
		:type  axis:  int
		
		:rtype:  TMCL.Reply
		"""


	def get_axis_param (self, param, axis=0):
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
		self.send(Command.GAP, type=param, motbank=axis)


	def get_global_param (self, bank, param ):
		"""
		All global parameters can be read with this function. In stand-alone 
		mode, the result is copied to the accumulator register for further 
		processing purposes such as conditional jumps. In direct mode, the 
		result is only output in the “value” field of the reply, without 
		affecting the accumulator. 
		
		:param bank:  Param bank [0..2]
		:type  bank:  int
		
		:param param: Parameter to get - See GlobalParams.* 
		:type  bank:  int
		
		:rtype: int 
		"""


	def set_global_param (self, bank, param, value):
		"""
		Global parameters are related to the host interface, peripherals or 
		application specific variables. The different groups of these 
		parameters are organised in "banks" to allow a larger total number 
		for future products.
		
		Currently, only bank 0 and 1 are used for global parameters, and 
		bank 2 is used for user variables. 
		
		:param bank:  Param bank [0..2]
		:type  bank:  int
		
		:param param: Parameter to set
		:type  param: int
		
		:param value: Parameter value
		:type  value: int
		
		:rtype: int 
		"""


	########################################################################
	#### Utility functions
	########################################################################


	def run_command( self, cmdIndex ):
		"""
		Execute a predefined subroutine previously written to 
		module firmware.
		
		:param cmdIndex:
		:return:
		"""
		reply = self.send(Command.RUN_APPLICATION, type=1, value=cmdIndex)
		return reply.status


	def get_param (self, param):
		"""
		Utility wrapper around `get_global_param` for ease of use
		
		:param param: One of GlobalParams.*
		:type  param: tuple(int,int)
		
		:return: Parameter value
		:rtype:  int
		"""
		reply = self.send(Command.GGP, type=param[1], motbank=param[0])
		return reply.value


	def set_param (self, param, value):
		"""
		Utility wrapper around `set_global_param` for ease of use
		
		:param param:  One of GlobalParams.*
		:type  param:  tuple(int,int)
		
		:param value:  Parameter value to set
		:type  value:  int
		"""
