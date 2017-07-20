
class Instruction (object):
	"""
	Represents a mutable TMCL instruction
	"""

	cmd = None
	"""
	TMCL command field
	
	:type: int
	"""

	type = 0
	"""
	TMCL type field
	
	:type: int
	"""

	motbank = 0
	"""
	TMCL motor/bank field
	
	:type: int
	"""

	value = 0
	"""
	TMCL value field
	
	:type: int
	"""

	def __init__ (self, cmd, type=0, motbank=0, value=0):
		self.cmd = cmd
		self.type = type
		self.motbank = motbank
		self.value = value
