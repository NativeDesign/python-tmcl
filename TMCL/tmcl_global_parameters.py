# -*- coding: UTF-8 -*-

class GlobalParams (object):
	"""
	The global parameters apply for all types of TMCM modules. They are 
	grouped into 3 banks: bank 0 (global configuration of the module), 
	bank 1 (user C variables) and bank 2 (user TMCL variables). 
	
	Access values:  
		R = readable (GAP) 
		W = writable (SAP)
		E = automatically restored from EEPROM after reset or power-on.

	"""


	#######################################################################
	## BANK 0
	## ------
	##
	## The following parameters with the numbers from 64 on configure things
	## like the serial address of the module RS232 / RS485 baud rate or CAN
	## bit rate. Change these parameters to meet your needs. The best and
	## easiest way to do this is to use the appropriate functions of the TMCL
	## IDE. The parameters with numbers between 64 and 128 are stored in
	## EEPROM only, so that an SGP command on such a parameter will always
	## store it permanently (no extra STGP command needed).
	##
	## Take care when changing these parameters, and use the appropriate
	## functions of the TMCL IDE to do it in an interactive way!
	#######################################################################



	EEPROM_RESET = (0,64)
	"""
	Setting this parameter to a different value as $E4 will cause 
	re-initialisation of the axis and global parameters (to factory 
	defaults) after the next power up. This is 	useful in case of 
	miss-configuration.
	
	Range:  0..255
	Access: RWE
	"""

	BAUD_RATE = (0,65)
	"""
	Set rs232 and rs485 baud rate
	
		0: 9600 baud (default)
		1: 14400 baud
		2: 19200 baud
		3: 28800 baud
		4: 38400 baud
		5: 57600 baud
		6: 76800 baud  Caution: Not supported by Windows!
		7: 115200 baud Caution: 115200 does not work with most host PCs,
					  as the baud rate error on the modules is too high 
					  with this baud rate (-3.5% baud rate error).
					  
	Range:  0..7
	Access: RWE
	"""

	SERIAL_ADDRESS = (0,66)
	"""
	The module (target) address for RS-232 and RS-485. 
	
	Range:  0..255
	Access: RWE
	"""

	ASCII_MODE = (0,67)
	"""
	Configure the TMCL ASCII interface:
	Bit 0: 0 – start up in binary (normal) mode
           1 – start up in ASCII mode
	Bits 4 and 5:
		00 – Echo back each character
		01 – Echo back complete command
		10 – Do not send echo, only send command reply
		
	Access: RWE
	"""

	CAN_BIT_RATE = (0,69)
	"""
	CAN bitrate
	
		1: 10kBit/s
		2: 20kBit/s
		3: 50kBit/s
		4: 100kBit/s
		5: 125kBit/s
		6: 250kBit/s (default)
		7: 500kBit/s
		8: 1000kBit/s (not supported by TMCM-30x/110/111/112)
		
	Range:  0..7
	Access: RWE
	"""

	CAN_REPLY_ID = (0,70)
	"""
	The CAN ID for replies from the board (default: 2) 
	
	Range:  0..7ff
	Access: RWE
	"""

	CAN_ID = (0,71)
	"""
	The module (target) address for CAN (default: 1) 
	
	Range:  0..7ff
	Access: RWE
	"""

	EEPROM_LOCK = (0,73)
	"""
	Write: 1234 to lock the EEPROM, 4321 to unlock it.
	Read: 1=EEPROM locked, 0=EEPROM unlocked.
	
	Range:  write: 1234/4321   read: 0/1
	Access: RWE
	"""

	ENCODER_INTERFACE = (0,74)
	"""
	Determines if a TMCM-323 is connected to the external SPI interface 
	and to which SPI_SEL line it is connected. Please see TMCM-323 manual 
	for details!
	
		0: No TMCM-323 connected
		1: Connected to SPI_SEL0
		2: Connected to SPI_SEL1
		3: Connected to SPI_SEL2
	
	Access: RWE	
	"""

	TELEGRAM_PAUSE_TIME = (0,75)
	"""
	Pause time before the reply via RS232 or RS485 will be sent. For RS232 
	set to 0, for RS485 it is often necessary to set it to 15 (for RS485 
	adapters controlled by the RTS pin).
	
	For CAN or IIC interface this parameter has no effect!
	
	Range:  0..255
	Access: RWE
	"""

	SERIAL_HOST_ADDRESS = (0,76)
	"""
	Host address used in the reply telegrams sent back via RS232 or RS485.
	
	Range:  0..255
	Access: RWE
	"""

	AUTO_START_MODE = (0,77)
	"""
	Set the auto-start mode
	
		0: Do not start TMCL application after power-up (default).
		1: Start TMCL application automatically after power-up
	
	Range:  0/1
	Access: RWE
	"""

	SHUTDOWN_PIN_MODE = (0,80)
	"""
	Select the functionality of the SHUTDOWN pin (not with TMCM-300).
	
		0: no function
		1: high active
		2: low active
	
	Range:  0..2
	Access: RWE
	"""

	CODE_PROTECTION = (0,81)
	"""
	Protect a TMCL program against disassembling or overwriting.
	
		0: no protection
		1: protection against disassembling
		2: protection against overwriting
		3: protection against disassembling and overwriting
		
	Note: When a user tries to switch off the protection against 
	      disassembling, the program will be erased first! So, when 
	      changing this value from 1 or 3 to 0 or 2, the TMCL program 
	      will be erased.
	      
	Range:  0..3
	Access: RWE
	"""

	APPLICATION_STATUS = (0,128)
	"""
	Current status of the TMCL application running on the module
	
		0: stop
		1: run
		2: step
		3: reset
		
	Range:  0..3
	Access: R
	"""

	DOWNLOAD_MODE = (0,129)
	"""
	Check if module is in download mode or not
	
		0: normal mode
		1: download mode
		
	Range:  0/1
	Access: R
	"""

	PROGRAM_COUNTER = (0,130)
	"""
	The index of the currently executed TMCL instruction.
	
	Access: R
	"""

	TICK_TIMER = (0,132)
	"""
	A 32 bit counter that gets incremented by one every millisecond. 
	It can also be reset to any start value.
	
	Access: RW
	"""
