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


### class Motor (bus, address, axis)

#### Methods

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

##### `set_axis_param ( param, value )`
Set axis parameter. See property definitions below for several
utility setters for common axis properties.

##### `get_axis_param (param, value)`
Get axis parameter. See property definitions below for 
several utility getters for common axis properties.


#### Properties

>	Note: The TMCM-100 module uses a different parameter set 
>	      (see chapter 4.3), but all other TMCL stepper motor 
>	      modules use these parameters.


##### `int target_position`
The desired position in position mode. Range ±2²³.

##### `int actual_position`
The current position of the motor. Should only be
overwritten for reference point setting. Range ±2²³.

##### `int target_speed`
The desired speed in velocity mode (see ramp mode, no.
138). In position mode, this parameter is set by
hardware: to the maximum speed during acceleration,
and to zero during deceleration and rest. Range ±2047.

##### `readonly int actual_speed`
The current rotation speed. Range ±2047.

##### `int max_positioning_speed`
Should not exceed the physically highest possible value.
Adjust the pulse divisor (no. 154), if the speed value is
very low (<50) or above the upper limit. See TMC 428
datasheet (p.24) for calculation of physical units. 
Range 0..2047.

##### `int max_accelleration`
The limit for acceleration (and deceleration). Changing
this parameter requires re-calculation of the acceleration
factor (no. 146) and the acceleration divisor (no.137),
which is done automatically. See TMC 428 datasheet
(p.24) for calculation of physical units.
Range 0..2047.

##### `int max_current`
The most important motor setting, since too high values
might cause motor damage! Note that on the TMCM-300
the phase current can not be reduced down to zero due
to the Allegro A3972 driver hardware.
On the TMCM-300, 303, 310, 110, 610, 611 and 612 the
maximum value is 1500 (which means 1.5A).
On all other modules the maximum value is 255 (which
means 100% of the maximum current of the module).

##### `int standby_current`
The current limit two seconds after the motor has
stopped. The value range of this parameter is the same as with
`max_current`.

##### `readonly bool target_position_reached`
Indicates that the actual position equals the target
position.

##### `readonly bool ref_switch_status`
The logical state of the reference (left) switch.
See the TMC 428 data sheet for the different switch
modes. Default is two switch mode: the left switch as
the reference switch, the right switch as a limit (stop)
switch.

##### `readonly bool right_limit_switch_status`
The logical state of the (right) limit switch.

##### `readonly bool left_limit_switch_status`
The logical state of the left limit switch (in three switch
mode).

##### `bool right_limit_switch_disabled`
If set, deactivates the stop function of the right switch

##### `bool left_limit_switch_disabled`
If set, deactivates the stop function of the left switch resp.
reference switch if set

[1]: https://www.trinamic.com/support/software/tmcl-ide/
