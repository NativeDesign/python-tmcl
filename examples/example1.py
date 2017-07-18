from serial import Serial
import TMCL


def simple_example ():
	## Open a serial port to connect to the bus
	serial_port = Serial("/dev/tty.usbmodem1241")
	bus = TMCL.connect(serial_port)

	## Get the motor on axis 0 of module with address 1
	motor = bus.get_motor(1)




def example_for_multi_axis_modules():
	## Open a serial port to connect to the bus
	serial_port = Serial("/dev/tty.usbmodem1241")
	bus = TMCL.connect(serial_port)

	## Get the module at address 1
	module = bus.get_module(1)

	## Get the motor on axis '0' of the module
	motor = module.get_motor(0)

	## Start sending commands to the motor
	motor.stop()
