Instruction
###########


**Constructor Summary**

+-----------------------------------------------------+------------------------------+
| Constructor                                         | Description                  |
+=====================================================+==============================+
| Instruction_ `( cmd, type=0, motbank=0, value=0 )`  | Create a new Module instance |
+-----------------------------------------------------+------------------------------+


**Property Summary**

+----------------------------------+--------------------------------------+
| Property                         + Description                          |
+==================================+======================================+
| cmd_ : `int`                     | TMCL command field                   |
+----------------------------------+--------------------------------------+
| type_ : `int`                    | TMCL type field                      |
+----------------------------------+--------------------------------------+
| motbank_ : `int`                 | TMCL motor/bank field                |
+----------------------------------+--------------------------------------+
| value_ : `int`                   | TMCL value field                     |
+----------------------------------+--------------------------------------+


------------------------------------------------------------


Constructor
===========

.. _Instruction:
.. function:: Instruction(cmd, type=0, motbank=0, value=0)

	:param cmd:  TMCL command field
	:type  cmd:  int [0..255]

	:param type: TMCL type field. Defaults to 0
	:type  type: int [0..255]

	:param type: TMCL motor/bank field. Defaults to 0
	:type  type: int [0..255]

	:param type: TMCL value field. Defaults to 0
	:type  type: int [-2^31..2^31]


Properties
==========

cmd
---
.. autoattribute:: TMCL.instruction.Instruction.cmd

type
----
.. autoattribute:: TMCL.instruction.Instruction.type

motbank
-------
.. autoattribute:: TMCL.instruction.Instruction.motbank

value
-----
.. autoattribute:: TMCL.instruction.Instruction.value

