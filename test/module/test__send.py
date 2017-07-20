from pytest import raises

from TMCL.module import Module
from TMCL.instruction import Instruction


class SuccessException (BaseException): pass




class Test__Module__send (object):

	def test__cmd_param_must_be_an_int (self):
		module = Module()

		with raises(ValueError) as err:
			module.send('not an integer')
		assert err.match(r'must be an int')

		with raises(ValueError) as err:
			module.send([123,456,789])
		assert err.match(r'must be an int')

		with raises(ValueError) as err:
			module.send(Module())
		assert err.match(r'must be an int')


	def test__type_param_must_be_an_int (self):
		module = Module()

		with raises(ValueError) as err:
			module.send(1, type='not an integer')
		assert err.match(r'must be an int')

		with raises(ValueError) as err:
			module.send(1, type=[123,456,789])
		assert err.match(r'must be an int')

		with raises(ValueError) as err:
			module.send(1, type=Module())
		assert err.match(r'must be an int')


	def test__motbank_param_must_be_an_int ( self ):
		module = Module()

		with raises(ValueError) as err:
			module.send(1, motbank='not an integer')
		assert err.match(r'must be an int')

		with raises(ValueError) as err:
			module.send(1, motbank=[123, 456, 789])
		assert err.match(r'must be an int')

		with raises(ValueError) as err:
			module.send(1, motbank=Module())
		assert err.match(r'must be an int')


	def test__value_param_must_be_an_int ( self ):
		module = Module()

		with raises(ValueError) as err:
			module.send(1, value='not an integer')
		assert err.match(r'must be an int')

		with raises(ValueError) as err:
			module.send(1, value=[123, 456, 789])
		assert err.match(r'must be an int')

		with raises(ValueError) as err:
			module.send(1, value=Module())
		assert err.match(r'must be an int')


	def test__calls_bus_send_with_correct_instruction (self):

		CMD = 111
		TYPE = 222
		MOTBANK = 3
		VALUE = 12345

		class Bus (object):
			def send(self, instruction):
				assert isinstance(instruction, Instruction)
				if instruction.cmd == CMD and \
					instruction.type == TYPE and \
					instruction.motbank == MOTBANK and \
					instruction.value == VALUE:
					raise SuccessException()



		module = Module(Bus())
		with raises(SuccessException):
			module.send(CMD, TYPE, MOTBANK, VALUE)


	def test__type_param_defaults_to_zero (self):
		class Bus:
			def send(self, instruction):
				if instruction.type == 0:
					raise SuccessException()

		module = Module(Bus())
		with raises(SuccessException):
			module.send(123)


	def test__motbank_param_defaults_to_zero ( self ):
		class Bus:
			def send ( self, instruction ):
				if instruction.motbank == 0:
					raise SuccessException()

		module = Module(Bus())
		with raises(SuccessException):
			module.send(123)


	def test__value_param_defaults_to_zero ( self ):
		class Bus:
			def send ( self, instruction ):
				if instruction.value == 0:
					raise SuccessException()

		module = Module(Bus())
		with raises(SuccessException):
			module.send(123)
