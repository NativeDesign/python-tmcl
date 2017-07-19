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
		self.bus = bus
		self.address = address


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

