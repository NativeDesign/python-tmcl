from pytest import raises

from TMCL import Motor
from TMCL.module import Module


class Test__Module__get_axis (object):


	def test__returns_Motor_instance (self):
		class Bus: pass
		module = Module(Bus())
		assert isinstance(module.get_axis(), Motor)


	def test__passes_axis_property_to_motor (self):
		class Bus: pass
		module = Module(Bus())

		AXIS = 123

		motor = module.get_axis(AXIS)
		assert motor.axis == AXIS


	def test__axis_param_defaults_to_zero (self):
		class Bus: pass
		module = Module(Bus())

		motor = module.get_axis()
		assert motor.axis == 0
