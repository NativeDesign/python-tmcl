from pytest import raises

from TMCL.module import Module



class Test__Module__Constructor (object):


	def test__sets_bus_property (self):

		class Bus: pass

		bus = Bus()
		module = Module(bus)

		assert module.bus == bus


	def test__sets_address_property (self):

		class Bus: pass
		bus = Bus()

		ADDRESS = 123

		module = Module(bus, ADDRESS)
		assert module.address == ADDRESS


	def test__address_param_defaults_to_1 (self):

		class Bus: pass
		bus = Bus()

		module = Module(bus)
		assert module.address == 1
