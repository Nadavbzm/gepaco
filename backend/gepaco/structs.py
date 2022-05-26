from hydration import *

class MockPacket(Struct):
    header = UInt8
    data = UInt16


message_to_opcode = {
    MockPacket: 123
}