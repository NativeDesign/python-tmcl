from pytest import raises

from TMCL import Reply, Motor, Command



class SuccessException (BaseException): pass

class BasicMockModule(object):
	def send ( self, *args ):
		return Reply()



class Test__send (object):


	def test__param_cmd_must_be_an_integer (self):
		"""
		`cmd` argument must be validated as integer
		"""
		motor = Motor(BasicMockModule())

		with raises(ValueError) as msg:
			motor.send('not-an-integer',123,456)
		assert msg.match(r'cmd must be an integer')


	def test__param_type_must_be_an_integer ( self ):
		"""
		`type` argument must be validated as integer
		"""
		motor = Motor(BasicMockModule())

		with raises(ValueError) as msg:
			motor.send(123, 'not-an-integer', 456)
		assert msg.match(r'type must be an integer')


	def test__param_type_defaults_to_zero (self):
		"""
		`type` argument defaults to zero
		"""
		class MockModule(object):
			def send ( self, cmd, type, motbank, value ):
				if type == 0:
					raise SuccessException()

		motor = Motor(MockModule())
		with raises(SuccessException):
			motor.send(Command.ROR, value=123)


	def test__param_value_must_be_an_integer ( self ):
		"""
		`value` argument must be validated as integer
		"""
		motor = Motor(BasicMockModule())

		with raises(ValueError) as msg:
			motor.send(123, 456, 'not-an-integer')
		assert msg.match(r'value must be an integer')


	def test__param_value_defaults_to_zero ( self ):
		"""
		`value` argument defaults to zero
		"""
		class MockModule(object):
			def send ( self, cmd, type, motbank, value ):
				if value == 0:
					raise SuccessException()
				else:
					print(value)

		motor = Motor(BasicMockModule())
		with raises(SuccessException):
			motor.send(Command.ROR, type=123)



	def test__param_cmd_must_be_in_allowed_list ( self ):
		motor = Motor(BasicMockModule())
		for cmd in motor.ALLOWED_COMMANDS:
			motor.send( cmd )
			assert True


