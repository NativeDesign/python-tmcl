Bus
###

Top-level interface for communicating with TMCM modules


**Constructor Summary**

+-------------------------------+------------------------------+
| Constructor                   | Description                  |
+===============================+==============================+
| Bus_ `( serial )`             | Create a new Bus instance    |
+-------------------------------+------------------------------+


**Property Summary**

+----------------------------------+--------------------------------------+
| Property                         + Description                          |
+==================================+======================================+
| serial_ : Serial                 | Serial port for communication        |
+----------------------------------+--------------------------------------+
| CAN_ : bool                      | True if serial is a CAN bus          |
+----------------------------------+--------------------------------------+



**Method Summary**

+-----------------------------------------------------------+---------------------------------------------------+
| Method                                                    | Description                                       |
+===========================================================+===================================================+
| send_ `( cmd, address, cmd, type=0, motbank=0, value=0 )` | Send message to the bus                           |
+-----------------------------------------------------------+---------------------------------------------------+
| get_module_ `( address=1 )`                               | Get a Module instance at specified address        |
+-----------------------------------------------------------+---------------------------------------------------+
| get_motor_  `( address=1, axis=0 )`                       | Get a Motor instance for axis and address         |
+-----------------------------------------------------------+---------------------------------------------------+



------------------------------------------------------------


Constructor
===========

.. _Bus:
.. function:: Bus ( serial )

	:param serial:  Serial port to use for communication
	:type  serial: Serial



Properties
==========

serial
------
.. autoattribute:: TMCL.bus.Bus.serial

CAN
---
.. autoattribute:: TMCL.bus.Bus.CAN



Methods
=======

send
----
.. automethod:: TMCL.bus.Bus.send

get_module
----------
.. automethod:: TMCL.bus.Bus.get_module

get_motor
---------
.. automethod:: TMCL.bus.Bus.get_motor


