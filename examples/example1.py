from serial import Serial
import TMCL

serial_port = Serial("/dev/tty.usbmodem1241")
bus = TMCL.connect(serial_port)
motor = bus.get_motor(0)

motor.stop()
