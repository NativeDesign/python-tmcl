Getting Started
===============



Connecting to the bus
---------------------
Connect your TMCM module to your computer using an RS485-to-serial converter.
You can connect multiple TMCM modules to the same RS485 bus, but you must ensure
that they are all set to use the same serial baud rate, and different serial port
addresses. This is easiest done using the TMCL-IDE (provided free by Trinamic)
and the on-board micro-usb connection.


Open a serial port to your RS485 connection using the pySerial library and
use it to create a Bus_ instance. This example assumes that all connected
TMCM modules are set to use a serial baud rate of 9600. ::

	from serial import Serial
	import TMCL

	serial_port = Serial("/dev/tty.ACM0", 9600)
	bus = TMCL.Bus( serial_port )




Adressing a TMCM module
-----------------------
Once you have a Bus_ instance, you can get a Module_ instance from it by passing
the serial-address of the module to the Bus's `get_module` method. This example
assumes that the TMCM module has been pre-configured to use a `serial-address`
of 5. ::

	from serial import Serial
	import TMCL

	serial_port = Serial("/dev/tty.ACM0")
	bus = TMCL.Bus( serial_port )

	module = bus.get_module(1)



Moving a motor
-----------------------
Each TMCM module hosts one or more motors. They are referred to by their `axis` on
the module. You can get a Motor_ interface from a Module_ instance by calling its
`get_motor` method. This will return a Motor_ instance that will allow you to read
and write `axis parameters` and move the motor. ::

	from serial import Serial
	import TMCL

	serial_port = Serial("/dev/tty.ACM0")
	bus = TMCL.Bus( serial_port )

	module = bus.get_module(1)

	motor = module.get_motor()



Once you have a Motor_ instance you can start it moving by issuing commands to the
instance. This example will make the motor rotate left at a speed of `1234` for 5
seconds before stopping again. ::

	from serial import Serial
	import TMCL

	serial_port = Serial("/dev/tty.ACM0")
	bus = TMCL.Bus( serial_port )

	module = bus.get_module(1)

	motor = module.get_motor()

	motor.rotate_left(1234)
	sleep(5)
	motor.stop()


.. _Bus: ./api/bus.html
.. _Module: ./api/module.html
.. _Motor: ./api/motor.html
