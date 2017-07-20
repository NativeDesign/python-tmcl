# coding=utf-8
from warnings import warn

from .motor import Motor
from .instruction import Instruction
from .tmcl_commands import commands, Command



class Module (object):

	bus = None
	""" 
	The Bus instance that will be used to communicate with the physical module
	:type: Bus
	"""

	address = None
	"""
	The module address on the bus
	:type: int
	"""

	def __init__ (self, bus, address=1):
		"""
		
		:param bus: Bus instance to use for communication
		:type  bus: Bus
		
		:param address: SerialAddress of module on bus
		:type  address: int
		"""
		assert isinstance(address, int),    'Address must be an int'
		assert 0 <= address <= 255,         'Address must be in [0..255]'

		self.bus = bus
		self.address = address



	#################################################################
	## Core functions
	#################################################################

	def send(self, cmd, type=0, motbank=0, value=0):
		""" Send an instruction this module
		
		Sends a TMCL instruction to this module and waits for a reply
		before returning a TMCL.Reply object.
		
		Args:
			cmd     (int):   TMCL command field
			type    (int):   TMCL type field
			motbank (int):   TMCL motor/bank field
			value   (int):   TMCL value field
			
		Returns:
			TMCL.Reply: The response from the module
			
		Raises:
			TrinamicException: If module returns anything but SUCCESS
		
		"""
		assert isinstance(cmd, Instruction) or isinstance(cmd, int), "cmd must be int or Instruction"
		assert isinstance(type, int),       'type must be an int'
		assert isinstance(motbank, int),    'motbank must be an int'
		assert isinstance(value, int),      'value must be an int'

		if isinstance(cmd, Instruction):
			return self.bus.send(self.address, cmd)
		else:
			return self.bus.send(self.address, Instruction(cmd, type, motbank, value))


	def get_motor (self, *args, **kwargs):
		return self.get_axis(*args,**kwargs)


	def get_axis (self, axis=0):
		"""
		Returns a Motor instance for the specified axis id
		
		:param axis: Motor axis id. Defaults to 0
		:type  axis: int
		
		:rtype: Motor 
		"""
		return Motor(self, axis=axis)


	def get_param (self, param, bank=None):
		"""
		Get the value of a global parameter from this module
		
		If `param` argument is an integer, `bank` arg MUST be 
		set.
		
		If `param` is a tuple(int,int) - like GlobalParams.* -
		then `bank` arg will be ignored.
		
		:param param:  Param id -OR- one of GlobalParams.*
		:type  param:  int | (int,int)
		
		:param bank:  Parameter bank number (ignored if `param` is a tuple)
		:type  bank:  int
		
		:return: The `value` property of the reply message from module
		:rtype: int
		"""
		if isinstance(param, tuple):
			if bank is not None:
				warn(UserWarning("arg 'bank' is ignored when param is a tuple"))

			assert len(param) == 2, "Tuple param must have exactly two values"
			bank = param[0]
			param = param[1]

		assert isinstance(param, int), "Param must be an int"
		assert isinstance(bank, int),  "Bank must be an int"
		assert bank in [0,1,2],        "Bank must be 0|1|2, got "+str(bank)

		inst = Instruction(Command.GGP, type=param, motbank=bank)
		return self.send(inst).value



	def set_param(self, param, value, bank=None):
		"""
		Set a global parameter on this module
		
		If `param` arg is an integer, `bank` arg MUST be set.
		
		If `param` arg is a tuple (one of GlobalParams.*), then
		`bank` arg will be ignored.
		
		:param param: Parameter ID  -OR- one of GlobalParams.*
		:type  param: int | (int,int)
		
		:param value: Parameter value to set
		:type  value: int
		
		:param bank:  Parameter bank number (ignored if `param` is a tuple)
		:type  bank:  int
		
		:return: Reply message from bus
		:rtype:  TMCL.Reply
		"""
		if isinstance(param, tuple):
			if bank is not None:
				warn(UserWarning("arg 'bank' is ignored when param is a tuple"))

			assert len(param) == 2, "Tuple param must have exactly two values"
			bank = param[0]
			param = param[1]

		assert isinstance(param, int),  'param must be an int'
		assert isinstance(value, int),  'value must be an int'
		assert isinstance(bank, int),   'bank must be an int'

		inst = Instruction(Command.SGP, type=param, motbank=bank, value=value)
		return self.send(inst)


	def get_axis_param (self, param, axis=0):
		"""
		Return the value of an axis parameter from a particular axis
		on the module
		
		From the TCML docs:
		
			Most parameters of a TMCM module can be adjusted individually for 
			each axis. Although these parameters vary widely in their formats 
			(1 to 24 bits, signed or unsigned) and physical locations (TMC428, 
			TMC453, controller RAM, controller EEPROM), they all can be read by 
			this function. ... In direct mode, the value read 
			is only output in the “value” field of the reply, without affecting 
			the accumulator. See chapter 4 for a complete list of all parameters.

		
		:param param:  Parameter ID. One of ``AxisParams.*``
		:type  param:  int
		
		:param axis:  Axis to get parameter from. Defaults to 0
		:type  axis:  int
		
		:return: The parameter value
		:rtype: int
		"""
		assert isinstance(param, int),  'param must be an int'
		assert 0 <= param <= 255,       'param must be in [0..255]'
		assert isinstance(axis, int),   'axis must be an int'
		assert 0 <= axis <= 255,        'axis must be in [0..255]'

		return self.send( Command.GAP, type=param, motbank=axis).value


	def set_axis_param (self, param, value, axis=0):
		"""
		Set an axis parameter on a particular axis on the module
		
		From the TCML docs:
		
			Most parameters of a TMCM module can be adjusted individually for 
			each axis. Although these parameters vary widely in their formats 
			(1 to 24 bits, signed or unsigned) and physical locations 
			(TMC428, TMC453, controller RAM, controller EEPROM), they all can 
			be set by this function. See chapter 4 for a complete list of all 
			axis parameters. See STAP (section 3.7) for permanent storage of a 
			modified value.

		
		:param param: Parameter ID. One of ``AxisParams.*``
		:type  param: int
		
		:param value: Value to set parameter to
		:type  value: int
		
		:param axis: Axis to set parameter to. Defaults to 0
		:type  axis: int
		
		:return: Reply message from Bus
		:rtype:  TMCL.Reply
		"""
		assert isinstance(param, int),  'param must be an int'
		assert 0 <= param <= 255,       'param must be in [0..255]'
		assert isinstance(value, int),  'value must be an int'
		assert isinstance(axis, int),   'axis must be an int'
		assert 0 <= axis <= 255,       'axis must be in [0..255]'

		return self.send( Command.SAP, type=param, motbank=axis, value=value)



	def write_firmware (self, instructions):
		""" Write TMCL firmware to module
		
		Write a series of TMCL instructions to this module's firmware.
		This will erase all current instructions held in firmware.
		
		Args:
			instructions ([Instruction]): List of instructions to write
	
		Returns:
			bool: True if successful
	
		Example::
		
			import TMCL.Command as c
			module = Module()
			module.write_application([
			    c.ROL( 0, 0, 123 )
			    c.MST( 0, 0, 0   )
			])
		
		"""
		raise NotImplementedError()


	def firmware_writer (self):
		""" 
		Returns a context manager that can be used to dynamically write
		an application to module firmware
	
		:rtype: contextmanager 
	
		Example::
		
			module = Module()
			with module.application_writer as s:
				s.ROL( 0, 0, 123 )
				s.MST( 0, 0, 0   )
		
		"""
		raise NotImplementedError()


##
## Shortcuts for TMCL commands
##
for cmd in commands:
	def invoke (self, type=0, motbank=0, value=0):
		self.send( cmd[1], type, motbank, value)
	setattr(Module, cmd[0], invoke)


