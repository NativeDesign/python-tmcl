Motor
#####


**Constructor Summary**

+-------------------------------+------------------------------+
| Constructor                   | Description                  |
+===============================+==============================+
| Motor_ `( module, axis=0 )`   | Create a new Motor instance  |
+-------------------------------+------------------------------+


**Property Summary**

+--------------------------------------+----------+----------------------------------------------------------+
| Property                             | Access   | Description                                              |
+======================================+==========+==========================================================+
| module_ : `Module`                   |          | The module this motor belongs to                         |
+--------------------------------------+----------+----------------------------------------------------------+
| axis_ : `int`                        |          | Axis id of motor on parent module                        |
+--------------------------------------+----------+----------------------------------------------------------+
| target_position_ : `int`             |          | Motor target position axis parameter                     |
+--------------------------------------+----------+----------------------------------------------------------+
| actual_position_ : `int`             |`readonly`| Current absolute position of motor                       |
+--------------------------------------+----------+----------------------------------------------------------+
| target_speed_ : `int`                |          | Motor target speed                                       |
+--------------------------------------+----------+----------------------------------------------------------+
| actual_speed_ : `int`                |`readonly`| Current speed of motor                                   |
+--------------------------------------+----------+----------------------------------------------------------+
| max_positioning_speed_ : `int`       |          | Max speed                                                |
+--------------------------------------+----------+----------------------------------------------------------+
| max_accelleration_ : `int`           |          | Max accelleration                                        |
+--------------------------------------+----------+----------------------------------------------------------+
| max_current_ : `int`                 |          | Max allowed current draw                                 |
+--------------------------------------+----------+----------------------------------------------------------+
| standby_current_ : `int`             |          | Standby current                                          |
+--------------------------------------+----------+----------------------------------------------------------+
| target_position_reached_ : `int`     |`readonly`| True if at target position                               |
+--------------------------------------+----------+----------------------------------------------------------+
| ref_switch_status_ : `int`           |`readonly`| The logical state of the reference (left) switch.        |
+--------------------------------------+----------+----------------------------------------------------------+
| right_limit_status_ : `int`          |`readonly`| The logical state of the (right) limit switch.           |
+--------------------------------------+----------+----------------------------------------------------------+
| left_limit_status_ : `int`           |`readonly`| The logical state of the left limit switch               |
+--------------------------------------+----------+----------------------------------------------------------+
| right_limit_switch_disabled_ : `int` |          | If set, deactivates the stop function of the right switch|
+--------------------------------------+----------+----------------------------------------------------------+
| left_limit_switch_disabled_ : `int`  |          | If set, deactivates the stop function of the left switch |
+--------------------------------------+----------+----------------------------------------------------------+


**Method Summary**

+-----------------------------------------------------+---------------------------------------------------+
| Method                                              | Description                                       |
+=====================================================+===================================================+
| send_ `( cmd, type=0, value=0 )`                    | Send a TMCL instruction to this motor             |
+-----------------------------------------------------+---------------------------------------------------+
| get_axis_param_ `( param  )`                        | Get an axis parameter from the module             |
+-----------------------------------------------------+---------------------------------------------------+
| set_axis_param_ `( param, value )`                  | Set an axis parameter on the module               |
+-----------------------------------------------------+---------------------------------------------------+
| stop_ `( )`                                         | Stop motor movement                               |
+-----------------------------------------------------+---------------------------------------------------+
| rotate_left_ `( velocity )`                         | Make the motor rotate left                        |
+-----------------------------------------------------+---------------------------------------------------+
| rotate_right_ `( velocity )`                        | Make the motor rotate right                       |
+-----------------------------------------------------+---------------------------------------------------+
| move_absolute_ `( position )`                       | Move motor to absolute position                   |
+-----------------------------------------------------+---------------------------------------------------+
| move_relative_ `( offset )`                         | Move motor by a relative amount                   |
+-----------------------------------------------------+---------------------------------------------------+
| reference_search_ `( type )`                        | Initiate a reference search                       |
+-----------------------------------------------------+---------------------------------------------------+



------------------------------------------------------------


Constructor
===========

.. _Motor:
.. function:: Motor(module, axis=0)

	:param module:  The Module instance this motor belongs to
	:type  bus: Module
	:param axis: Motor axis ID on the module
	:type  axis: int




Properties
==========

module
------
.. autoattribute:: TMCL.motor.Motor.module

axis
----
.. autoattribute:: TMCL.motor.Motor.axis

target_position
---------------
.. autoattribute:: TMCL.motor.Motor.target_position

actual_position
---------------
.. autoattribute:: TMCL.motor.Motor.actual_position

target_speed
------------
.. autoattribute:: TMCL.motor.Motor.target_speed

actual_speed
------------
.. autoattribute:: TMCL.motor.Motor.actual_speed

max_positioning_speed
---------------------
.. autoattribute:: TMCL.motor.Motor.max_positioning_speed

max_accelleration
-----------------
.. autoattribute:: TMCL.motor.Motor.max_accelleration

max_current
-----------
.. autoattribute:: TMCL.motor.Motor.max_current

standby_current
---------------
.. autoattribute:: TMCL.motor.Motor.standby_current

target_position_reached
-----------------------
.. autoattribute:: TMCL.motor.Motor.target_position_reached

ref_switch_status
-----------------
.. autoattribute:: TMCL.motor.Motor.ref_switch_status

right_limit_status
------------------
.. autoattribute:: TMCL.motor.Motor.right_limit_status

left_limit_status
-----------------
.. autoattribute:: TMCL.motor.Motor.left_limit_status

right_limit_switch_disabled
---------------------------
.. autoattribute:: TMCL.motor.Motor.right_limit_switch_disabled

left_limit_switch_disabled
--------------------------
.. autoattribute:: TMCL.motor.Motor.left_limit_switch_disabled





Methods
=======

send
----
.. automethod:: TMCL.motor.Motor.send

get_axis_param
--------------
.. automethod:: TMCL.motor.Motor.get_axis_param

set_axis_param
--------------
.. automethod:: TMCL.motor.Motor.set_axis_param

stop
----
.. automethod:: TMCL.motor.Motor.stop

rotate_left
-----------
.. automethod:: TMCL.motor.Motor.rotate_left

rotate_right
------------
.. automethod:: TMCL.motor.Motor.rotate_right

move_absolute
-------------
.. automethod:: TMCL.motor.Motor.move_absolute

move_relative
-------------
.. automethod:: TMCL.motor.Motor.move_relative

reference_search
----------------
.. automethod:: TMCL.motor.Motor.reference_search
