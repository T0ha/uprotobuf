import unittest
from protobuf.uprotobuf import Field
from random import randint

ENCODED_1 = b'\x01'
ENCODED_127 = b'\x7f'
ENCODED_128 = b'\x80\x01'
ENCODED_256 = b'\x80\x02'
ENCODED_65535 = b'\xff\xff\x03'
ENCODED_65536 = b'\x80\x80\x04'

class TestField(unittest.TestCase):
    def test_encode_varint(self):
        field = Field('test', 'Bool', 1)
        assert ENCODED_1 == field._encode_varint(1)
        assert ENCODED_127 == field._encode_varint(127)
        assert ENCODED_128 == field._encode_varint(128)
        assert ENCODED_256 == field._encode_varint(256)
        assert ENCODED_65535 == field._encode_varint(65535)
        assert ENCODED_65536 == field._encode_varint(65536)

    def test_decode_encode_varint(self):
        numbers = [randint(1, 65536) for _ in range(1, randint(10, 30))]
        field = Field('test', 'Bool', 1)

        for n in numbers:
            assert (n, b'') == field._decode_varint(field._encode_varint(n))
    
    def test_encode_bool(self):
        field = Field('test', 'Bool', 1)
        assert b'\x08\x00' == field.encode(False)
        assert b'\x08\x01' == field.encode(True)

    def test_encode_int32(self):
        field = Field('test', 'Int32', 1)
        assert b'\x08' + ENCODED_1 == field.encode(1)
        assert b'\x08' + ENCODED_127 == field.encode(127)
        assert b'\x08' + ENCODED_128 == field.encode(128)
        assert b'\x08' + ENCODED_256 == field.encode(256)
        assert b'\x08' + ENCODED_65535 == field.encode(65535)
        assert b'\x08' + ENCODED_65536 == field.encode(65536)

    def test_encode_uint32(self):
        field = Field('test', 'UInt32', 1)
        assert b'\x08' + ENCODED_1 == field.encode(1)
        assert b'\x08' + ENCODED_127 == field.encode(127)
        assert b'\x08' + ENCODED_128 == field.encode(128)
        assert b'\x08' + ENCODED_256 == field.encode(256)
        assert b'\x08' + ENCODED_65535 == field.encode(65535)
        assert b'\x08' + ENCODED_65536 == field.encode(65536)

    @unittest.skip('Needs test data')
    def test_encode_sint32(self):
        field = Field('test', 'SInt32', 1)
        assert b'\x08' + ENCODED_1 == field.encode(1)
        assert b'\x08' + ENCODED_127 == field.encode(127)
        assert b'\x08' + ENCODED_128 == field.encode(128)
        assert b'\x08' + ENCODED_256 == field.encode(256)
        assert b'\x08' + ENCODED_65535 == field.encode(65535)
        assert b'\x08' + ENCODED_65536 == field.encode(65536)

    def test_encode_int64(self):
        field = Field('test', 'Int64', 1)
        assert b'\x08' + ENCODED_1 == field.encode(1)
        assert b'\x08' + ENCODED_127 == field.encode(127)
        assert b'\x08' + ENCODED_128 == field.encode(128)
        assert b'\x08' + ENCODED_256 == field.encode(256)
        assert b'\x08' + ENCODED_65535 == field.encode(65535)
        assert b'\x08' + ENCODED_65536 == field.encode(65536)

    def test_encode_uint64(self):
        field = Field('test', 'UInt64', 1)
        assert b'\x08' + ENCODED_1 == field.encode(1)
        assert b'\x08' + ENCODED_127 == field.encode(127)
        assert b'\x08' + ENCODED_128 == field.encode(128)
        assert b'\x08' + ENCODED_256 == field.encode(256)
        assert b'\x08' + ENCODED_65535 == field.encode(65535)
        assert b'\x08' + ENCODED_65536 == field.encode(65536)

    @unittest.skip('Needs test data')
    def test_encode_sint64(self):
        field = Field('test', 'SInt64', 1)
        assert b'\x08' + ENCODED_1 == field.encode(1)
        assert b'\x08' + ENCODED_127 == field.encode(127)
        assert b'\x08' + ENCODED_128 == field.encode(128)
        assert b'\x08' + ENCODED_256 == field.encode(256)
        assert b'\x08' + ENCODED_65535 == field.encode(65535)
        assert b'\x08' + ENCODED_65536 == field.encode(65536)

    def test_decode_encode_bool(self):
        field = Field('test', 'Bool', 1)
        assert (False, b'') == field.decode(field.encode(False))
        assert (True, b'') == field.decode(field.encode(True))

    def test_decode_encode_int32(self):
        numbers = [randint(1, 65536) for _ in range(1, randint(10, 30))]
        field = Field('test', 'Int32', 1)

        for n in numbers:
            assert (n, b'') == field.decode(field.encode(n))

    def test_decode_encode_uint32(self):
        numbers = [randint(1, 65536) for _ in range(1, randint(10, 30))]
        field = Field('test', 'UInt32', 1)

        for n in numbers:
            assert (n, b'') == field.decode(field.encode(n))

    def test_decode_encode_sint32(self):
        numbers = [randint(1, 65536) for _ in range(1, randint(10, 30))]
        field = Field('test', 'Int32', 1)

        for n in numbers:
            assert (n, b'') == field.decode(field.encode(n))

    def test_decode_encode_int64(self):
        numbers = [randint(1, 65536) for _ in range(1, randint(10, 30))]
        field = Field('test', 'Int64', 1)

        for n in numbers:
            assert (n, b'') == field.decode(field.encode(n))
    def test_decode_encode_uint64(self):
        numbers = [randint(1, 65536) for _ in range(1, randint(10, 30))]
        field = Field('test', 'UInt64', 1)

        for n in numbers:
            assert (n, b'') == field.decode(field.encode(n))

    @unittest.skip('Needs test data')
    def test_decode_encode_sint64(self):
        numbers = [randint(1, 65536) for _ in range(1, randint(10, 30))]
        field = Field('test', 'SInt64', 1)

        for n in numbers:
            assert (n, b'') == field.decode(field.encode(n))

    def test_decode_encode_string(self):
        field = Field('test', 'String', 1)
        assert ('test string', b'') == field.decode(field.encode('test string'))

    def test_decode_encode_bytes(self):
        field = Field('test', 'Bytes', 1)
        assert (b'test string', b'') == field.decode(field.encode(b'test string'))
