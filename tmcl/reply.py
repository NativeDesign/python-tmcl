


class TrinamicException (Exception):
    def __init__ (self, reply):
        super(TrinamicException, self).__init__( Status.messages[reply.status] )
        self.reply = reply


class Reply (object):
    def __init__(self, reply_struct):
        self.reply_address = reply[0]
        self.module_address = reply[1]
        self.status = reply[2]
        self.command = reply[3]
        self.value = reply[4]
        self.checksum = reply[5]

    class Status (object):
        SUCCESS = 100
        COMMAND_LOADED = 101
        WRONG_CHECKSUM = 1
        INVALID_COMMAND = 2
        WRONG_TYPE = 3
        INVALID_VALUE = 4
        EEPROM_LOCKED = 5
        COMMAND_NOT_AVAILABLE = 6


        messages = {
            1: "Incorrect Checksum",
            2: "Invalid Command",
            3: "Wrong Type",
            4: "Invalid Value",
            5: "EEPROM Locked",
            6: "Command not Available"
        }
