Python TMCL client library
==========================

Python wrapper around Trinamic's TMCL serial interface for controlling TMCM stepper modules 
via a serial-to-rs485 converter.



Installation
------------

### Install using pip
```sh
> pip install tmcl
```

### Install without pip
```sh
> git clone https://github.com/NativeDesign/python-tmcl.git
> cd python-tmcl
> python setup.py install
```


Usage
-----

Use an RS485-to-serial adapter to connect your PC to one or more TMCM modules.
Before starting you should check the modules' serial-address and baud-rate is 
a known value. Out of the box (_warning: anecdotal_) modules usually have an address
of `1` and a baud-rate of `9600` but this is not guarenteed. The easiest way to check
these values is by using the [TMCL IDE][1] on a windows machine.

If using multiple TMCM modules attached to the same rs485 bus you __must__ ensure that
each module is set to a _different_ serial-address so that they don't clash.


### Example usage (single-axis modules)
```python
from serial import Serial
from time import sleep
import TMCL

## serial-address as set on the TMCM module.
MODULE_ADDRESS = 1

## Open the serial port presented by your rs485 adapter
serial_port = Serial("/dev/tty.usbmodem1241")

## Create a Bus instance using the open serial port
bus = TMCL.connect(serial_port)

## Get the motor
motor = bus.get_motor(MODULE_ADDRESS)

## From this point you can start issuing TMCL commands 
## to the motor as per the TMCL docs. This example will
## rotate the motor left at a speed of 1234 for 2 seconds
motor.rotate_left(1234)
sleep(2)
motor.stop()
```


### Example usage (multi-axis modules)
```python
from serial import Serial
import TMCL

## Open the serial port presented by your rs485 adapter
serial_port = Serial("/dev/tty.usbmodem1241")

## Create a Bus instance using the open serial port
bus = TMCL.connect(serial_port)

## Get the motor on axis 0 of module with address 1
module = bus.get_module( 1 )

a0 = module.get_motor(0)
a1 = module.get_motor(1)
a2 = module.get_motor(2)

```




API Overview
------------


#### class Motor (bus, address, axis)

##### `move_absolute (position)`
Move the motor to the specified _absolute_ position.

##### `move_relative (offset)`
Move the motor by the specified offset _relative to current position_.

##### `reference_search (rfs_type)`
Start a reference search routine to locate limit switches.

##### `rotate_left (velocity)`
Rotate the motor left-wards at the specified velocity.

##### `rotate_right (velocity)`
Rotate the motor right-wards at the specified velocity.

##### `run_command (cmd)`
Execute a predefined user subroutine written to TMCM module firmware

##### `send (cmd, type, motorbank, value)`
Send a raw TMCL command to the motor. 

##### `stop ()`
Stop the motor


[1]: https://www.trinamic.com/support/software/tmcl-ide/
