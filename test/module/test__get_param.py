from pytest import raises, warns

from TMCL import Reply
from TMCL.tmcl_commands import Command
from TMCL.module import Module


class SuccessException (BaseException): pass


class Bus (object):
	def send (self, address, cmd, type=0, motbank=0, value=0):
		return Reply()


class Test__Module__get_param (object):


	def test__if_param_is_int_then_bank_must_be_set (self):
		module = Module(Bus())

		## Should pass
		module.get_param(123, bank=1)
		module.get_param(123,2)

		## Should raise
		with raises(AssertionError):
			module.get_param(123)


	def test__if_param_is_tuple_it_must_be_valid (self):
		module = Module(Bus())

		## Should pass
		module.get_param((1,2))
		module.get_param((0,22))

		## Should raise
		with raises(AssertionError):
			module.get_param( (1,2,3) )

		with raises(AssertionError):
			module.get_param( (1, 'not an int') )

		with raises(AssertionError):
			module.get_param( () )


	def test__if_param_is_tuple_setting_bank_will_warn (self):
		module = Module(Bus())

		## Should pass
		with warns(None) as warnings:
			module.get_param( (0, 123) )
			module.get_param( 123, 0 )
		assert len(warnings) == 0

		with warns(UserWarning) as warnings:
			module.get_param( (0, 123), 123)
			module.get_param( (0, 123), bank=1)
		assert len(warnings) == 2



	def test__bank_arg_must_be_0_1_2 (self):
		module = Module(Bus())

		with raises(AssertionError):
			module.get_param(123, 10)

		with raises(AssertionError):
			module.get_param(123, 'not an integer')



	def test__sends_correct_instruction_to_bus (self):

		ADDRESS = 4
		CMD = Command.GGP
		PARAM = 22
		BANK = 2
		VALUE = 0

		class Bus:
			def send (self, address, instruction):
				assert address == ADDRESS
				assert instruction.cmd == CMD
				assert instruction.type == PARAM
				assert instruction.motbank == BANK
				assert instruction.value == 0
				raise SuccessException()

		module = Module(Bus(), address=ADDRESS)

		with raises(SuccessException):
			module.get_param((BANK, PARAM))

		with raises(SuccessException):
			module.get_param( PARAM, BANK )



	def test__returns_reply_value (self):
		VALUE = 142

		class Bus:
			def send (self, address, instruction):
				reply = Reply()
				reply.value = VALUE
				return reply

		module = Module(Bus())
		assert module.get_param(123,0) == VALUE
