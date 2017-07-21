

commands = [
	('ROR',1),      # Rotate right
	('ROL',2),      # Rotate left
	('MST',3),      # Motor stop
	('MVP',4),      # Move to position
	('SAP',5),      # Set axis parameter
	('GAP',6),      # Get axis parameter
	('STAP',7),     # Store axis parameter into EEPROM
	('RSAP',8),     # Restors axis parameter from EEPROM
	('SGP',9),      # Set global parameter
	('GGP',10),     # Get global parameter
	('STGP',11),    # Store global parameter into EEPROM
	('RSGP',12),    # Restore global parameter from EEPROM
	('RFS',13),     # Reference search
	('SIO',14),     # Set output
	('GIO',15),     # Get input
	('SCO',30),     # Store coordinate
	('CCO',32),     # Capture coordinate
	('GCO',31),     # Get coordinate
	('SAC',29),     # Access to external SPI device
	('JA',22),      # Jump always
	('JC',21),      # Jump conditional
	('COMP',20),    # Compare accumulator with constant value
	('CLE',36),     # Clear error flags
	('CSUB',23),    # Call subroutine
	('RSUB',24),    # Return from subroutine
	('WAIT',27),    # Wait for a specified event
	('STOP',28),    # End of a TMCL program
	('CALC',19),    # Calculate using the accumulator and a constant value
	('CALCX',33),   # Calculate using the accumulator and the X register
	('AAP',34),     # Copy accumulator to an axis parameter
	('AGP',35),     # Copy accumulator to a global parameter

	('UF0', 64),    # User function 1
	('UF1', 65),    # User function 2
	('UF2', 66),    # User function 3
	('UF3', 67),    # User function 4
	('UF4', 68),    # User function 5
	('UF5', 69),    # User function 6
	('UF6', 70),    # User function 7
	('UF7', 71),    # User function 8

	('STOP_APPLICATION',128), 
	('RUN_APPLICATION',129), 
	('STEP_APPLICATION',130), 
	('RESET_APPLICATION',131), 
	('START_DOWNLOAD_MODE',132), 
	('QUIT_DOWNLOAD_MODE',133), 
	('READ_TMCL_MEMORY',134), 
	('GET_APPLICATION_STATUS',135), 
	('GET_FIRMWARE_VERSION',136), 
	('RESTORE_FACTORY_SETTINGS',137), 
]


class Command (object): pass
for cmd in commands:
	setattr(Command, cmd[0], cmd[1])




def get_label (cmd):
	"""
	Get the human-readable label associated with a TMCL command
	
	:param cmd: The TMCL command to get a label for
	:type  cmd: int
	
	:return: Human-readable label for TMCL command
	:rtype:  str
	"""
	cmds = filter(lambda x: x[1] == cmd, commands)
	if cmds:
		return cmds[0]
	else:
		return None


