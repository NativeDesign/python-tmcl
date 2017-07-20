
from pytest import raises

from TMCL import Reply, Motor
from TMCL import Command


class BasicMockModule(object):
	def send ( self, *args ):
		return Reply()




class Test__rotate_left (object):


	def test__velocity_must_be_an_int (self):
		""" 
		Velocity must be validated as an integer 
		"""
		motor = Motor(BasicMockModule())
		with raises(ValueError) as msg:
			motor.rotate_left("not an integer")
		msg.match(r'must be an int')



	def test__velocity_must_be_within_bounds (self):
		"""
		Velocity param must be within range 0 <= velocity <= self._max_velocity
		"""
		motor = Motor(BasicMockModule())
		motor._max_velocity = 100

		with raises(ValueError) as msg:
			motor.rotate_left(-123)

		with raises(ValueError) as msg:
			motor.rotate_left(101)

		motor.rotate_left(50)



	def test__calls_send_with_correct_args (self):
		"""
		Must call motor.send() with the correct arguments
		:return: 
		"""

		VELOCITY = 123

		motor = Motor(BasicMockModule())

		def mock_send (cmd, type=0, value=0):
			assert cmd == Command.ROL and \
				value == VELOCITY
			return Reply()
		setattr(motor,'send',mock_send)

		motor.rotate_left( VELOCITY )



