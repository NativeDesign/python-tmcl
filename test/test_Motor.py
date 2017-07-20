# -*- coding: utf-8 -*-

import pytest

import TMCL
from TMCL import Motor


EXPECTED_REPLY_VALUE = 4321


class SuccessException (BaseException): pass



class MockModule (object):
	def send (self, cmd, type, motbank=0, value=0):
		reply = TMCL.Reply()
		reply.status = TMCL.Reply.Status.SUCCESS
		reply.value = EXPECTED_REPLY_VALUE
		return reply




class Test__Motor (object):


	def setup_method (self):
		self.motor = TMCL.Motor(MockModule())



	def test__send_adds_correct_axis_to_command (self):
		"""
		Motor instances should append the correct axis id 
		to commands it sends to module
		"""
		AXIS = 3
		class MockModule (object):
			def send (self, cmd, type, motbank=0, value=0):
				assert motbank == AXIS
				return TMCL.Reply()

		motor = Motor(MockModule(), axis=AXIS)
		motor.send(TMCL.Command.GAP)



	def test__get_axis_param__checks_param_type(self):
		"""
		get_axis_param should throw an exception if the 'param'
		parameter is not of type `int`
		"""
		with pytest.raises(ValueError, message="Should raise ValueError if param is not an integer"):
			self.motor.get_axis_param("Not-an-integer")


	def test__get_axis_param__returns_reply_value (self):
		"""
		get_axis_param should return the value property from the 
		Reply object returned from the bus
		"""
		assert self.motor.get_axis_param(2) == EXPECTED_REPLY_VALUE, \
			"Should return the Reply object's value property"


	def test__get_axis_param__sends_correct_command (self):
		"""
		Check get_axis_param sends the correct command to module
		"""
		class MockModule:
			def send (self, cmd, type, motbank=0, value=0):
				assert \
					cmd == TMCL.Command.GAP and \
					type == TMCL.AxisParams.TARGET_POSITION and \
					motbank == 0 and \
					value == 0, \
				"Module.send not called with expected params"
				return TMCL.Reply()


		module = MockModule()
		motor = TMCL.Motor(module)
		motor.get_axis_param(TMCL.AxisParams.TARGET_POSITION)




	def test__set_axis_param__checks_param_type(self):
		"""
		set_axis_param should throw an error if `param` parameter is 
		not of type int
		"""
		with pytest.raises(ValueError, message="Should raise ValueError if param is not of type int"):
			self.motor.set_axis_param("Not an integer",123)


	def test__set_axis_param__checks_value_type(self):
		"""
		set_axis_param should throw an error if `value` parameter is 
		not of type int
		"""
		with pytest.raises(ValueError, message="Should raise ValueError if param is not of type int"):
			self.motor.set_axis_param(123, "Not an integer")


	def test__set_axis_param__sends_correct_command (self):
		"""
		Check set_axis_param sends the correct command to module
		"""
		class MockModule:
			def send (self, cmd, type, motbank=0, value=0):
				assert \
					cmd == TMCL.Command.SAP and \
					type == TMCL.AxisParams.TARGET_POSITION and \
					motbank == 0 and \
					value == 123, \
				"Module.send not called with expected params"
				return TMCL.Reply()

		module = MockModule()
		motor = TMCL.Motor(module)
		motor.set_axis_param(TMCL.AxisParams.TARGET_POSITION, 123)




	def test__stop__sends_correct_command (self):
		"""
		stop() method should call module.send with the correct arguments
		"""

		AXIS = 100
		
		class MockModule:
			def send (self, cmd, type, motbank=0, value=0):
				if cmd == TMCL.Command.MST and \
					motbank == AXIS:
					raise SuccessException()
			
		module = MockModule()
		motor = TMCL.Motor(module, axis=AXIS)
		with pytest.raises(SuccessException):
			motor.stop()



	# def test__rotate_left__validates_velocity_type (self):

