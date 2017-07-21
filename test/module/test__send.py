from pytest import raises

from TMCL import Reply
from TMCL.module import Module
from TMCL.instruction import Instruction


class SuccessException (BaseException): pass


class Bus:
	def send(self, address, instruction):
		return Reply()


class Test__Module__send (object):

	def test__cmd_param_must_be_an_int (self):
		module = Module(Bus())

		with raises(AssertionError):
			module.send('not an integer')

		with raises(AssertionError):
			module.send([123,456,789])

		with raises(AssertionError):
			module.send(Bus())


	def test__type_param_must_be_an_int (self):
		module = Module(Bus())

		with raises(AssertionError):
			module.send(1, type='not an integer')

		with raises(AssertionError):
			module.send(1, type=[123,456,789])

		with raises(AssertionError):
			module.send(1, type=Bus())


	def test__motbank_param_must_be_an_int ( self ):
		module = Module(Bus())

		with raises(AssertionError):
			module.send(1, motbank='not an integer')

		with raises(AssertionError):
			module.send(1, motbank=[123, 456, 789])

		with raises(AssertionError):
			module.send(1, motbank=Bus())


	def test__value_param_must_be_an_int ( self ):
		module = Module(Bus())

		with raises(AssertionError):
			module.send(1, value='not an integer')

		with raises(AssertionError):
			module.send(1, value=[123, 456, 789])

		with raises(AssertionError):
			module.send(1, value=Bus())


	def test__calls_bus_send_with_correct_instruction (self):

		CMD = 111
		TYPE = 222
		MOTBANK = 3
		VALUE = 12345

		class Bus (object):
			def send(self, address, instruction):
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
			def send(self, address, instruction):
				if instruction.type == 0:
					raise SuccessException()

		module = Module(Bus())
		with raises(SuccessException):
			module.send(123)


	def test__motbank_param_defaults_to_zero ( self ):
		class Bus:
			def send ( self, address, instruction ):
				if instruction.motbank == 0:
					raise SuccessException()

		module = Module(Bus())
		with raises(SuccessException):
			module.send(123)


	def test__value_param_defaults_to_zero ( self ):
		class Bus:
			def send ( self, address, instruction ):
				if instruction.value == 0:
					raise SuccessException()

		module = Module(Bus())
		with raises(SuccessException):
			module.send(123)
