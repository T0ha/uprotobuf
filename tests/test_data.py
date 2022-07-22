from protobuf.uprotobuf import Enum

ENCODED_1 = b'\x01'
ENCODED_2 = b'\x02'
ENCODED_3 = b'\x03'
ENCODED_5 = b'\x05'
ENCODED_127 = b'\x7f'
ENCODED_128 = b'\x80\x01'
ENCODED_256 = b'\x80\x02'
ENCODED_65535 = b'\xff\xff\x03'
ENCODED_65536 = b'\x80\x80\x04'

class Enum1(Enum):
    default = 1
    one = 1
    two = 2
    three = 3
