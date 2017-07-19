import struct
from .motor import Module, Motor
from .reply import Reply, TrinamicException


# MSG_STRUCTURE = ">BBBBIB"
MSG_STRUCTURE = ">BBBBiB"
MSG_STRUCTURE_CAN = ">BBBI"

# REPLY_STRUCTURE = ">BBBBIB"
REPLY_STRUCTURE = ">BBBBiB"
REPLY_STRUCTURE_CAN = ">BBBI"
REPLY_STRUCTURE_IIC = ">BBBIB"

REPLY_LENGTH = 9
REPLY_LENGTH_CAN = 7
REPLY_LENGTH_IIC = 8


class Bus (object):

	def __init__( self, serial, CAN = False ):
		self.CAN = CAN
		self.serial = serial

	def send ( self, address, command, type, motorbank, value ):
		"""
		Send a message to the specified module.
		This is a blocking function that will not return until a reply
		has been received from the module.
		
		See the TMCL docs for full descriptions of the parameters
		
		:param address:   Module address to send command to
		:param command:   Instruction no
		:param type:	  Type
		:param motorbank: Mot/Bank
		:param value:	  Value
	
		:rtype: Reply
		"""
		if self.CAN:
			msg = struct.pack(MSG_STRUCTURE_CAN, command, type, motorbank,value)
			self.serial.write(msg)
			resp = [0]
			data = self.serial.read(REPLY_LENGTH_CAN)
			resp.extend(struct.unpack(REPLY_STRUCTURE_CAN, data))
			reply = Reply(resp)
			return self._handle_reply(reply)
		else:
			checksum = self._binaryadd(address, command, type, motorbank, value)
			msg = struct.pack(MSG_STRUCTURE, address, command, type, motorbank, value, checksum)
			self.serial.write(msg)
			rep = self.serial.read(REPLY_LENGTH)
			reply = Reply(struct.unpack(REPLY_STRUCTURE, rep))
			return self._handle_reply(reply)

	def get_module( self, address=1 ):
		"""
			Returns a Module object targeting the device at address `address`
			You can use this object to retrieve one or more axis motors.

			:param address:  
				Bus address to the target TMCM module
			:type  address: int

			:rtype: Module
		"""
		return Module(self, address)

	def get_motor( self, address=1, motor_id=0 ):
		"""		
			Returns object addressing motor number `motor_id` on module `address`.
			`address` defaults to 1 (doc for TMCM310 starts counting addresses at 1).
			`motor_id` defaults to 0 (1st axis).

			This is an alias for `get_module(address).get_motor(motor_id)` so that 
			backward-compatibility with v1.1.1 is maintained.

			:param address:  
				Bus address of the target TMCM module
			:type  address:  int

			:param motor_id:
				ID of the motor/axis to target
			:type  motor_id: int

			:rtype: Motor
		"""
		return Motor(self, address, motor_id)

	def _handle_reply (self, reply):
		if reply.status < Reply.Status.SUCCESS:
			raise TrinamicException(reply)
		return reply

	def _binaryadd( self, address, command, type, motorbank, value ):
		checksum_struct = struct.pack(MSG_STRUCTURE[:-1], address, command, type, motorbank, value)
		checksum = 0
		for s in checksum_struct:
			checksum += int(s) % 256
			checksum = checksum % 256
		return checksum


