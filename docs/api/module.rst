Module
######

An interface to a single TMCM stepper module with one or more axes.



**Example:**

.. code-block:: python

	from TMCM import Module, GlobalParams
	module = Module( bus, address=4 )
	module.set_param (GlobalParams.SHUTDOWN_PIN_MODE, 2)
	motor = module.get_motor()





**Constructor Summary**

+-------------------------------+------------------------------+
| Constructor                   | Description                  |
+===============================+==============================+
| Module_ `( bus, address=1 )`  | Create a new Module instance |
+-------------------------------+------------------------------+


**Property Summary**

+----------------------------------+--------------------------------------+
| Property                         + Description                          |
+==================================+======================================+
| bus_ : Bus                       | The Bus used for communication       |
+----------------------------------+--------------------------------------+
| address_ : Bus                   | Serial address of module on the bus  |
+----------------------------------+--------------------------------------+


**Method Summary**

+-----------------------------------------------------+---------------------------------------------------+
| Method                                              | Description                                       |
+=====================================================+===================================================+
| send_ `( cmd, type=0, motbank=0, value=0 )`         | Send a TMCL instruction to this module            |
+-----------------------------------------------------+---------------------------------------------------+
| get_motor_ `( axis=0 )`                             | Get a Motor instance for an axis on this module   |
+-----------------------------------------------------+---------------------------------------------------+
| get_axis_  `( axis=0 )`                             | Get a Motor instance for an axis on this module   |
+-----------------------------------------------------+---------------------------------------------------+
| get_param_ `( param, bank=None )`                   | Get a global parameter from the module            |
+-----------------------------------------------------+---------------------------------------------------+
| set_param_ `( param, value, bank=None )`            | Set a global parameter on the module              |
+-----------------------------------------------------+---------------------------------------------------+
| get_axis_param_ `( param, axis=0 )`                 | Get an axis parameter from the module             |
+-----------------------------------------------------+---------------------------------------------------+
| set_axis_param_ `( param, value, axis=0 )`          | Set an axis parameter on the module               |
+-----------------------------------------------------+---------------------------------------------------+
| write_firmware_ `( param, value, axis=0 )`          | Write a series of instructions to module firmware |
+-----------------------------------------------------+---------------------------------------------------+
| firmware_writer_ `( )`                              | Get a ContextManager for writing firmware         |
+-----------------------------------------------------+---------------------------------------------------+


------------------------------------------------------------


Constructor
===========

.. _Module:
.. function:: Module(bus, address=1)

	:param bus:  The Bus instance to use for communication
	:type  bus: Bus
	:param address: Module address on bus. Defaults to 1
	:type  address: int




Properties
==========

bus
---
.. autoattribute:: TMCL.module.Module.bus

address
-------
.. autoattribute:: TMCL.module.Module.address




Methods
=======
send
----
.. automethod:: TMCL.module.Module.send

get_motor
---------
.. method:: Module.get_motor(axis=0)

	Alias of get_axis_

get_axis
--------
.. automethod:: TMCL.module.Module.get_axis

get_param
---------
.. automethod:: TMCL.module.Module.get_param

set_param
---------
.. automethod:: TMCL.module.Module.set_param

get_axis_param
--------------
.. automethod:: TMCL.module.Module.get_axis_param

set_axis_param
--------------
.. automethod:: TMCL.module.Module.set_axis_param

write_firmware
--------------
.. automethod:: TMCL.module.Module.write_firmware

firmware_writer
---------------
.. automethod:: TMCL.module.Module.firmware_writer


