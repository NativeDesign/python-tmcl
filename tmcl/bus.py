import struct
from .motor import Motor
from .reply import Reply, TrinamicException


MSG_STRUCTURE = ">BBBBIB"
MSG_STRUCTURE_CAN = ">BBBI"

REPLY_STRUCTURE = ">BBBBIB"
REPLY_STRUCTURE_CAN = ">BBBI"
REPLY_STRUCTURE_IIC = ">BBBIB"

REPLY_LENGTH = 9
REPLY_LENGTH_CAN = 7
REPLY_LENGTH_IIC = 8


class Bus (object):

    def __init__( self, serial, CAN = False ):
        self.CAN = CAN
        self.serial = serial
    
    def binaryadd(address, command, type, motorbank, value):
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
            checksum = binaryadd(address, command, type, motorbank, value)
            msg = struct.pack(MSG_STRUCTURE, address, command, type, motorbank, value, checksum)
            self.serial.write(msg)
            rep = self.serial.read(REPLY_LENGTH)
            reply = Reply(struct.unpack(REPLY_STRUCTURE, rep))
            return self._handle_reply(reply)
    
    def _handle_reply (self, reply):
        if reply.status < Reply.Status.SUCCESS:
            raise TrinamicException(reply)
        return reply
    
    def get_motor (self, address):
        return Motor(self, address)
