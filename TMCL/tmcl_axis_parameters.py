# -*- coding: UTF-8 -*-

from .tmcl_commands import Command


class AxisParams (object):
	"""
	The following sections describe all axis parameters that can be used with the 
	SAP, GAP, AAP, STAP and RSAP commands. Please note that some parameters are 
	different with different module types. 
	
	Please note that the TMCM-100 module uses a different parameter set (see chapter 4.3),
	but all other TMCL stepper motor modules use these parameters.
	
	Some of these parameters (marked ADVANCED) influence the TMC428 directly so 
	that advanced understanding of the TMC428 chip is needed.
	
	Access values:  
		R = readable (GAP) 
		W = writable (SAP)
		E = automatically restored from EEPROM after reset or power-on.
	
	:see: http://www.mctechnology.nl/pdf/TMCL_reference_2015.pdf (Page 52)
	"""


	TARGET_POSITION = 0
	"""
	The desired position in position mode (see RAMP_MODE).
	
	Range:  ±2^23
	Access: RW
	"""

	ACTUAL_POSITION = 1
	"""
	The current position of the motor. Should only be overwritten for 
	reference point setting.
	
	Range:  ±2^23
	Access: RW
	"""

	TARGET_SPEED = 2
	"""
	The desired speed in velocity mode (see RAMP_MODE). In position 
	mode, this parameter is set by hardware: to the maximum speed 
	during acceleration, and to zero during deceleration and rest.
	
	Range:  ±2047
	Access: RW
	"""

	ACTUAL_SPEED = 3
	"""
	The current rotation speed. Should never be overwritten.
	
	Range:  0..2047
	Access: R
	"""

	MAX_POSITIONING_SPEED = 4
	"""
	Should not exceed the physically highest possible value. Adjust the 
	pulse divisor (no. 154), if the speed value is very low (<50) or 
	above the upper limit. 
	See TMC 428 datasheet (p.24) for calculation of physical units.
	
	Range:  0..2047
	Access: RWE
	"""

	MAX_ACCELLERATION = 5
	"""
	The limit for acceleration (and deceleration). Changing this parameter 
	requires re-calculation of the acceleration factor (no. 146) and the 
	acceleration divisor (no.137), which is done automatically. 
	See TMC 428 datasheet (p.24) for calculation of physical units.
	
	Range:  0..2047
	Access: RWE
	"""

	MAX_CURRENT = 6
	"""
	The most important motor setting, since too high values might cause 
	motor damage! Note that on the TMCM-300 the phase current can not be 
	reduced down to zero due to the Allegro A3972 driver hardware.
	On the TMCM-300, 303, 310, 110, 610, 611 and 612 the maximum value 
	is 1500 (which means 1.5A). On all other modules the maximum value is 
	255 (which means 100% of the maximum current of the module)
	
	Range:  0..1500 / 0..255 (see above)
	Access: RWE
	"""

	STANDBY_CURRENT = 7
	"""
	The current limit two seconds after the motor has stopped.
	The value range of this parameter is the same as with MAX_CURRENT
	
	Range:  0..1500 / 0..255 (see above)
	Access: RWE
	"""

	TARGET_POSITION_REACHED = 8
	"""
	Indicates that the actual position equals the target position.
	
	Range:  0/1
	Access: R
	"""

	REF_SWITCH_STATUS = 9
	"""
	The logical state of the reference (left) switch. See the TMC 428 
	data sheet for the different switch modes. Default is two switch mode: 
	the left switch as the reference switch, the right switch as a 
	limit (stop) switch.
	
	Range:  0/1
	Access: R
	"""

	RIGHT_LIMIT_SWITCH_STATUS = 10
	"""
	The logical state of the (right) limit switch.
	
	Range:  0/1
	Access: R
	"""

	LEFT_LIMIT_SWITCH_STATUS = 11
	"""
	The logical state of the left limit switch (in three switch mode)
	
	Range:  0/1
	Access: R
	"""

	RIGHT_LIMIT_SWITCH_DISABLE = 12
	"""
	If set, deactivates the stop function of the right switch
	 
	Range:  0/1
	Access: RWE
	"""

	LEFT_LIMIT_SWITCH_DISABLE = 13
	"""
	Deactivates the stop function of the left switch resp. reference 
	switch if set.
	
	Range:  0/1
	Access: RWE
	"""


	#############################################################################
	##
	## Advanced axis parameters
	## ========================
	##
	## These parameters are only needed if the desired needs can not be met
	## by setting the basic parameters listed in section 4.1. Some of these
	## parameters influence the TMC428 directly so that advanced understanding
	## of the TMC428 chip is needed. There are even some parameters that
	## should only be changed if recommended by TRINAMIC. Please note that
	## these paramters are not available on the TMCM-100 module.
	#############################################################################

	MIN_SPEED = 130
	"""
	Should always be set 1 to ensure exact reaching of the target position. 
	Do not change!
	
	Range:  0..2047
	Access: RWE
	"""

	ACTUAL_ACCELERATION = 135
	"""
	The current acceleration (read only).
	
	Range:  0..2047
	Access: R
	"""

	ACCELERATION_THRESHOLD = 136
	"""
	Specifies the threshold between low and high acceleration values for 
	the parameters 144&145. Normally not needed.
	
	Range:  0..2047
	Access: RWE
	"""

	ACCELERATION_DIVISOR = 137
	"""
	A ramping parameter, can be adjusted in special cases, automatically 
	calculated by setting the maximum acceleration (e.g. during normal 
	initialisation). See the TMC428 data sheet for details. 
	Normally no need to change.
	
	Range:  0..13
	Access: RWE
	"""

	RAMP_MODE = 138
	"""
	In version 2.16 and later: automatically set when using ROR, ROL, MST and MVP.
	
		0: Position mode. Steps are generated, when the parameters actual position
		   and target position differ. Trapezoidal speed ramps are provided.
		   
		2: Velocity mode. The motor will run continuously and the speed will be 
		   changed with constant (maximum) acceleration, if the parameter 
		   "target speed" is changed.
		   
		For special purposes, the soft mode (value 1) with exponential decrease of 
		speed can be selected. 
	
	Range:  0/1/2
	Access: RWE
	"""

	INTERRUPT_FLAGS = 139
	"""
	Must not be modified. See the TMC 428 datasheet for details
	
	Range:  16 bits
	Access: RW
	"""

	MICROSTEP_RESOLUTION = 140
	"""		
	Note that modifying this parameter will affect the rotation speed in the 
	same relation. Even if the module is specified for 16 microsteps only, switching 
	to 32 or 64 microsteps still brings an enhancement in resolution and smoothness. 
	The position counter will use the full resolution, but, however, the motor will 
	resolve a maximum of 24 different microsteps only for the 32 or 64 microstep units.

		0: full step *
		1: half step *
		2: 4 microsteps
		3: 8 microsteps
		4: 16 microsteps
		5: 32 microsteps
		6: 64 microsteps

	* Please note that the fullstep setting as well as the half step setting are not 
	optimized for use without an adapted microstepping table. These settings just step 
	through the microstep table in steps of 64 respectively 32. To get real full 
	stepping use axis parameter 211 or load an adapted microstepping table.
	
	Range:  0..6
	Access: RWE
	"""

	REF_SWITCH_TOLERANCE = 141
	"""
	For three-switch mode: a position range, where an additional switch (connected to 
	the REFL input) won't cause motor stop. See section 6.1 for details.
	
	Range:  0..4095
	Access: RW
	"""

	SNAPSHOP_POSITION = 142
	"""
	For referencing purposes, the exact position at hitting of the reference switch 
	can be captured in this parameter. 
	A dummy value has to be written first to prepare caption.
	
	Range:  ±2^23
	Access: RW
	"""

	MAX_CURRENT_AT_REST = 143
	"""
	In contrast to the standby current, this current limit becomes immediately active 
	when the motor speed reaches zero. The value represents a fraction of the absolute
	maximum current:
	
		0:     no change of current at rest (default, 100%)
		1..7:  12.5%..87.5%

	See the TMC428 datasheet for details. 
	Normally not used, use MAX_CURRENT and STANDBY_CURRENT instead!
	
	Range:  0..7
	Access: RWE
	"""

	MAX_CURRENT_AT_LOW_ACCELERATION = 144
	"""
	An optional current reduction factor, see parameters 136 and 143 for details. 
	Normally not used, use MAX_CURRENT and STANDBY_CURRENT instead!
	
	Range:  0..7
	Access: RWE
	"""

	MAX_CURRENT_AT_HIGH_ACCELERATION = 145
	"""
	An optional current reduction factor, see parameters ACCELERATION_THRESHOLD 
	and MAX_CURRENT_AT_REST for details. 
	Normally not used, use MAX_CURRENT and STANDBY_CURRENT instead!
	
	Range:  0..7
	Access: RWE
	"""

	ACCELERATION_FACTOR = 146
	"""
	A ramping parameter, can be adjusted in special cases, automatically calculated 
	by setting the maximum acceleration (e.g. during normal initialisation). 
	See the TMC428 data sheet for details. Normally no need to change.
	
	Range:  0..128
	Access: RWE
	"""

	REF_SWITCH_DISABLE_FLAG = 147
	"""
	If set, the reference switch (left switch) won't cause the motor to stop. 
	See RIGHT_LIMIT_SWITCH_DISABLE and LEFT_LIMIT_SWITCH_DISABLE
	
	Range:  0/1 
	Access: RWE
	"""

	LIMIT_SWITCH_DISABLE_FLAG = 148
	"""
	If set, the limit switch (right switch) won't cause the motor to stop. 
	See RIGHT_LIMIT_SWITCH_DISABLE and LEFT_LIMIT_SWITCH_DISABLE
	
	Range:  0/1 
	Access: RWE
	"""

	SOFT_STOP_FLAG = 149
	"""
	If cleared, the motor will stop immediately (disregarding motor limits), 
	when the reference or limit switch is hit.
	
	Range:  0/1 
	Access: RWE
	"""

	POSITION_LATCH_FLAG = 151
	"""
	Indicates that a position snapshot has been completed (see SNAPSHOP_POSITION).
	
	Range:  0/1 
	Access: RWE
	"""

	INTERRUPT_MASK = 152
	"""
	Must not be modified. See the TMC 428 datasheet for details
	
	Range:  16 bits
	Access: R
	"""

	RAMP_DIVISOR = 153
	"""
	The exponent of the scaling factor for the ramp generator should be 
	de/incremented carefully (in steps of one). 
	
	Range:  0..13
	Access: RWE
	"""

	PULSE_DIVISOR = 154
	"""
	The exponent of the scaling factor for the pulse (step) generator 
	– should be de/incremented carefully (in steps of one).
	
	Range:  0..13
	Access: RWE
	"""

	REFERENCING_MODE = 193
	"""
	Set the reference search mode. Please see chapter 6.1 for details on 
	reference search.
	
		1: Only the left reference switch is searched.
		
		2: The right switch is searched, then the left switch is searched.
		
		3: Three-switch-mode: the right switch is searched first, then the 
		   reference switch will be searched.
		   
	Range:  1/2/3
	Access: RWE
	"""

	REFERENCE_SEARCH_SPEED = 194
	"""
	For the reference search this value specifies the search speed as a 
	fraction of the maximum velocity:
	
		0: full speed
		1: half of the maximum speed
		2: a quarter of the maximum speed
		3: 1/8 of the maximum speed (etc.)

	On the TMCM-34x modules the speed is given directly as a value 
	between 0..2047.
	
	Range:  0..8 (0..2047 M-34X)
	Access: RWE
	"""

	REFERENCE_SWITCH_SPEED = 195
	"""
	Similar to parameter no. 194, the speed for the switching point 
	calibration can be selected.
	
	On the TMCM-34x modules the speed is given directly as a value 
	between 0..2047.
	
	Range:  0..8 (0..2047 M-34X)
	Access: RWE
	"""

	DRIVER_OFF_TIME = 198
	"""
	TMCM-300 ONLY!
	
	A special adjustment of the motor driver A3972. 
	Low values may cause more mechanical vibrations, while the higher ones 
	lead to acoustic noise of the drivers. The default value of 20 is a good 
	compromise for most applications. See the Allegro A3972 datasheet for details.
	
	Range:  0..31
	Access: RWE
	"""

	FAST_DECAY_TIME = 200
	"""
	A special adjustment of the motor driver A3972 (TMCM-300 only), with less 
	influence than the driver off time (no. 198) in most cases. Low values generally 
	reduce driver noise. See the Allegro A3972 datasheet for details.
	
	Range:  0..15
	Access: RWE
	"""

	MIXED_DECAY_THRESHOLD = 203
	"""
	If the actual velocity is above this threshold, mixed decay will be used 
	(all modules except the TMCM-300). Since V3.13, this can also be set to –1 which 
	turns on mixed decay permanently also in the rising part of the microstep wave.
	This can be used to fix microstep errors.
	
	Range:  0..2048/-1
	Access: RWE
	"""

	FREEWHEELING = 204
	"""
	TMCM-301 / 303 / 310 / 11x and 61x only
	
	Time after which the power to the motor will be cut when its velocity has 
	reached zero.

		0: never
			
	Range:  0..65535 
	Access: RWE
	"""

	STALL_DETECTION_THRESHOLD = 205
	"""
	Stall detection threshold. Only usable on modules equipped with TMC246 or TMC249 
	motor drivers. Set it to 0 for no stall detection or to a value between 1 
	(low threshold) and 7 (high threshold). The motor will be stopped if the load value
	exceeds the stall detection threshold. Switch off mixed decay to get usable results.
	
	Range:  0..7
	Access: RWE
	"""

	ACTUAL_LOAD_VALUE = 206
	"""
	Readout of the actual load value used for stall detection. Only usable on modules 
	equipped with TMC246 or TMC249 motor drivers. On other modules this value is undefined.
	
	Range:  0..7
	Access: R
	"""

	DRIVER_ERROR_FLAGS = 208
	"""
	TMC236 Error Flags
	
	Access: R
	"""

	ENCODER_POSITION = 209
	"""
	The value of an encoder register of a TMCM-323 module connected to a TMCM-30x module 
	can be read or written. Please see the TMCM-323 manual for details.
	
	Access: RW
	"""

	ENCODER_PRESCALER = 210
	"""
	TMCM-323, TMCM-611, TMCM-101 & TMCM-102
	
	Pre-scaler for an encoder connected to a TMCM-323 module.
	Please see the TMCM-323 manual for details. This value can not be read back!
	Please see the manuals of specific module for the meaning of these parameter.
	
	Access: W
	"""

	FULLSTEP_THRESHOLD = 211
	"""
	When exceeding this speed the driver will switch to real full step mode. 
	To disable this feature set this parameter to zero or to a value greater than 2047.
	Setting a full step threshold allows higher motor torque of the motor at higher velocity. 
	When experimenting with this	in a given application, try to reduce the motor current in
	order to be able to reach a higher motor velocity!
	
	Range:  0..2048
	Access: RWE
	"""

	MAXIMUM_ENCODER_DEVIATION = 212
	"""
	TMCM-101, TMCM-102 and TMCM-611 only.
	
	When the actual position (parameter 1) and the encoder position (parameter 209) 
	differ more than set here the motor will be stopped. This function is switched 
	off when the maximum deviation is set to zero.
	
	Range:  0..65535
	Access: RWE
	"""

	GROUP_INDEX = 213
	"""
	TMCM-610, TMCM-611, TMCM-612 and TMCM-34x only.
	
	All motors on one module that have the same group index will also get the same 
	commands when a ROL, ROR, MST, MVP or RFS is issued for one of these motors. 
	
	Range:  0..255
	Access: RW
	"""






class TMCM100_AxisParameters:
	"""
	The axis parameters on the TMCM-100 module and on the Monopack 2 
	with TMCL differ from those on the other modules. There are no “advanced” 
	axis parameters on the TMCM-100 module.
	"""

	TARGET_POSITION = 0
	ACTUAL_POSITION = 1
	TARGET_VELOCITY = 2
	ACTUAL_VELOCITY = 3
	MAX_POSITIONING_VELOCITY = 4
	MAX_ACCELERATION = 5
	CURRENT_AT_CONSTANT_ROTATION = 6
	CURRENT_AT_STANDBY = 7
	POSITION_REACHED_FLAG = 8
	REFERENCE_SWITCH_STATUS = 9
	RIGHT_STOP_SWITCH_STATUS = 10
	LEFT_STOP_SWITCH_STATUS = 11
	STOP_SWITCH_DISABLE = 12
	STEP_RATE_PRESCALER = 14
	BOW = 15
	MICROSTEP_RESOLUTION = 16
	MICROSTEP_WAVEFORM = 17
	STEP_MODE = 18
	STEP_PULSE_LENGTH = 19
	PHASES = 20
	CURRENT_AT_ACCELERATION = 21
	REFERENCE_SEARCH_MODE = 22
	REFERENCE_SEARCH_VELOCITY = 23
	STOP_SWITCH_DECCELERATION = 24
	ENCODER_POSITION = 25
	ENCODER_CONFIGURATION = 26
	ENCODER_PREDIVIDER = 27
	ENCODER_MULTIPLIER = 28
	MAXIMUM_DEVIATION = 29
	DEVIATION_ACTION = 30
	CORRECTION_DELAY = 31
	CORRECTION_RETRIES = 32
	CORRECTION_TOLERANCE = 33
	CORRECTION_VELOCITY = 34





class AxisParameterInterface(object):
	"""
	Utility interface to Axis parameters for individual
	module motor/axes.
	"""
	def __init__ ( self, motor ):
		"""

		:param motor:
		:type  motor: Motor
		"""
		self.motor = motor


	def get ( self, param ):
		reply = self.motor.send(Command.GAP, param, self.motor.motor_id, 0)
		return reply.value


	def set ( self, param, value ):
		reply = self.motor.send(Command.SAP, param, self.motor.motor_id, value)
		return reply.status


	@property
	def target_position ( self ):
		return self.get(0)


	@target_position.setter
	def target_position ( self, value ):
		self.set(0, value)


	@property
	def actual_position ( self ):
		return self.get(1)


	@actual_position.setter
	def actual_position ( self, value ):
		self.set(1, value)


	@property
	def target_speed ( self ):
		return self.get(2)


	@target_speed.setter
	def target_speed ( self, value ):
		self.set(2, value)


	@property
	def actual_speed ( self ):
		return self.get(3)


	@property
	def max_positioning_speed ( self ):
		return self.get(4)


	@max_positioning_speed.setter
	def max_positioning_speed ( self, value ):
		self.set(4, value)


	@property
	def max_accelleration ( self ):
		return self.get(5)


	@max_accelleration.setter
	def max_accelleration ( self, value ):
		self.set(5, value)


	@property
	def max_current ( self ):
		return self.get(6)


	@max_current.setter
	def max_current ( self, value ):
		self.set(6, value)


	@property
	def standby_current ( self ):
		return self.get(7)


	@standby_current.setter
	def standby_current ( self, value ):
		self.set(7, value)


	@property
	def target_position_reached ( self ):
		return self.get(8)


	@property
	def ref_switch_status ( self ):
		return self.get(9)


	@property
	def right_limit_status ( self ):
		return self.get(10)


	@property
	def left_limit_status ( self ):
		return self.get(11)


	@property
	def right_limit_switch_disabled ( self ):
		return True if self.get(12) == 1 else False


	@right_limit_switch_disabled.setter
	def right_limit_switch_disabled ( self, value ):
		self.set(12, 1 if value else 0)


	@property
	def left_limit_switch_disabled ( self ):
		return True if self.get(13) == 1 else False


	@left_limit_switch_disabled.setter
	def left_limit_switch_disabled ( self, value ):
		self.set(13, 1 if value else 0)
