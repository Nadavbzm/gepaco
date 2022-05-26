from hydration import *

class MockPacket(Struct):
    header = UInt8
    data = UInt16