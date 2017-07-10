import struct
from .motor import Motor
from .reply import Reply, TrinamicException


# MSG_STRUCTURE = ">BBBBIB"
MSG_STRUCTURE = ">BBBBiB"
MSG_STRUCTURE_CAN = ">BBBI"

# REPLY_STRUCTURE = ">BBBBIB"
REPLY_STRUCTURE = ">BBBBiB"
REPLY_STRUCTURE_CAN = ">BBBI"
REPLY_STRUCTURE_IIC = ">BBBIB"

REPLY_LENGTH = 9
REPLY_LENGTH_CAN = 7
REPLY_LENGTH_IIC = 8


class Bus (object):

    def __init__( self, serial, CAN = False ):
        self.CAN = CAN
        self.serial = serial
    
    def binaryadd(self, address, command, type, motorbank, value):
        checksum_struct = struct.pack(MSG_STRUCTURE[:-1], address, command, type, motorbank, value)
        checksum = 0
        for s in checksum_struct:
            checksum += int(s) % 256
            checksum  = checksum % 256
        return checksum
    
    def send ( self, address, command, type, motorbank, value ):
        if self.CAN:
            msg = struct.pack(MSG_STRUCTURE_CAN, command, type, motorbank,value)
            self.serial.write(msg)
            resp = [0]
            data = self.serial.read(REPLY_LENGTH_CAN)
            resp.extend(struct.unpack(REPLY_STRUCTURE_CAN, data))
            reply = Reply(resp)
            return self._handle_reply(reply)
        else:
            checksum = self.binaryadd(address, command, type, motorbank, value)
            msg = struct.pack(MSG_STRUCTURE, address, command, type, motorbank, value, checksum) # max_current gets applied wrong! Some internal rounding!?
            self.serial.write(msg)
            rep = self.serial.read(REPLY_LENGTH)
            reply = Reply(struct.unpack(REPLY_STRUCTURE, rep))
            return self._handle_reply(reply)
    
    def _handle_reply (self, reply):
        if reply.status < Reply.Status.SUCCESS:
            raise TrinamicException(reply)
        return reply
    
    def get_module (self, module_address = 1, motor = 0):
        """
            Returns object addressing motor number 'motor' on module 'module_address'.
            module_address defaults to 1 (doc for TMCM310 starts counting addresses at 1).
            motor defaults to 0 (1st axis).
        """
        return Motor(self, module_address, motor)
