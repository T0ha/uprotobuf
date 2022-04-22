import unittest
from protobuf.uprotobuf import Field
from random import getrandbits
from .test_data import *

class TestField(unittest.TestCase):
    def test_encode_varint(self):
        field = Field('test', 'Bool', 1)
        self.assertEqual(ENCODED_1, field._encode_varint(1))
        self.assertEqual(ENCODED_127, field._encode_varint(127))
        self.assertEqual(ENCODED_128, field._encode_varint(128))
        self.assertEqual(ENCODED_256, field._encode_varint(256))
        self.assertEqual(ENCODED_65535, field._encode_varint(65535))
        self.assertEqual(ENCODED_65536, field._encode_varint(65536))

    def test_decode_encode_varint(self):
        numbers = [getrandbits(31) for _ in range(1, getrandbits(8))]
        field = Field('test', 'Bool', 1)

        for n in numbers:
            print(n)
            self.assertEqual((n, b''), field._decode_varint(field._encode_varint(n)))
    
    def test_encode_bool(self):
        field = Field('test', 'Bool', 1)
        self.assertEqual(b'', field.encode(False))
        self.assertEqual(b'\x08\x01', field.encode(True))

    def test_encode_int32(self):
        field = Field('test', 'Int32', 1)
        self.assertEqual(b'\x08' + ENCODED_1, field.encode(1))
        self.assertEqual(b'\x08' + ENCODED_127, field.encode(127))
        self.assertEqual(b'\x08' + ENCODED_128, field.encode(128))
        self.assertEqual(b'\x08' + ENCODED_256, field.encode(256))
        self.assertEqual(b'\x08' + ENCODED_65535, field.encode(65535))
        self.assertEqual(b'\x08' + ENCODED_65536, field.encode(65536))

    def test_encode_uint32(self):
        field = Field('test', 'UInt32', 1)
        self.assertEqual(b'\x08' + ENCODED_1, field.encode(1))
        self.assertEqual(b'\x08' + ENCODED_127, field.encode(127))
        self.assertEqual(b'\x08' + ENCODED_128, field.encode(128))
        self.assertEqual(b'\x08' + ENCODED_256, field.encode(256))
        self.assertEqual(b'\x08' + ENCODED_65535, field.encode(65535))
        self.assertEqual(b'\x08' + ENCODED_65536, field.encode(65536))

    @unittest.skip('Needs test data')
    def test_encode_sint32(self):
        field = Field('test', 'SInt32', 1)
        self.assertEqual(b'\x08' + ENCODED_1, field.encode(1))
        self.assertEqual(b'\x08' + ENCODED_127, field.encode(127))
        self.assertEqual(b'\x08' + ENCODED_128, field.encode(128))
        self.assertEqual(b'\x08' + ENCODED_256, field.encode(256))
        self.assertEqual(b'\x08' + ENCODED_65535, field.encode(65535))
        self.assertEqual(b'\x08' + ENCODED_65536, field.encode(65536))

    def test_encode_int64(self):
        field = Field('test', 'Int64', 1)
        self.assertEqual(b'\x08' + ENCODED_1, field.encode(1))
        self.assertEqual(b'\x08' + ENCODED_127, field.encode(127))
        self.assertEqual(b'\x08' + ENCODED_128, field.encode(128))
        self.assertEqual(b'\x08' + ENCODED_256, field.encode(256))
        self.assertEqual(b'\x08' + ENCODED_65535, field.encode(65535))
        self.assertEqual(b'\x08' + ENCODED_65536, field.encode(65536))

    def test_encode_uint64(self):
        field = Field('test', 'UInt64', 1)
        self.assertEqual(b'\x08' + ENCODED_1, field.encode(1))
        self.assertEqual(b'\x08' + ENCODED_127, field.encode(127))
        self.assertEqual(b'\x08' + ENCODED_128, field.encode(128))
        self.assertEqual(b'\x08' + ENCODED_256, field.encode(256))
        self.assertEqual(b'\x08' + ENCODED_65535, field.encode(65535))
        self.assertEqual(b'\x08' + ENCODED_65536, field.encode(65536))

    @unittest.skip('Needs test data')
    def test_encode_sint64(self):
        field = Field('test', 'SInt64', 1)
        self.assertEqual(b'\x08' + ENCODED_1, field.encode(1))
        self.assertEqual(b'\x08' + ENCODED_127, field.encode(127))
        self.assertEqual(b'\x08' + ENCODED_128, field.encode(128))
        self.assertEqual(b'\x08' + ENCODED_256, field.encode(256))
        self.assertEqual(b'\x08' + ENCODED_65535, field.encode(65535))
        self.assertEqual(b'\x08' + ENCODED_65536, field.encode(65536))

    def test_decode_encode_bool(self):
        field = Field('test', 'Bool', 1, default=4) # default is added to make it decode False
        self.assertEqual((False, b''), field.decode(0x08, field.encode(False)[1:]))
        self.assertEqual((True, b''), field.decode(0x08, field.encode(True)[1:]))

    def test_decode_encode_int32(self):
        numbers = [getrandbits(31) for _ in range(1, getrandbits(8))]
        field = Field('test', 'Int32', 1)

        for n in numbers:
            self.assertEqual((n, b''), field.decode(0x08, field.encode(n)[1:]))

    def test_decode_encode_uint32(self):
        numbers = [getrandbits(31) for _ in range(1, getrandbits(8))]
        field = Field('test', 'UInt32', 1)

        for n in numbers:
            self.assertEqual((n, b''), field.decode(0x08, field.encode(n)[1:]))

    def test_decode_encode_sint32(self):
        numbers = [getrandbits(31) for _ in range(1, getrandbits(8))]
        field = Field('test', 'Int32', 1)

        for n in numbers:
            self.assertEqual((n, b''), field.decode(0x08, field.encode(n)[1:]))

    def test_decode_encode_int64(self):
        numbers = [getrandbits(31) for _ in range(1, getrandbits(8))]
        field = Field('test', 'Int64', 1)

        for n in numbers:
            self.assertEqual((n, b''), field.decode(0x08, field.encode(n)[1:]))
    def test_decode_encode_uint64(self):
        numbers = [getrandbits(31) for _ in range(1, getrandbits(8))]
        field = Field('test', 'UInt64', 1)

        for n in numbers:
            self.assertEqual((n, b''), field.decode(0x08, field.encode(n)[1:]))

    @unittest.skip('Needs test data')
    def test_decode_encode_sint64(self):
        numbers = [getrandbits(31) for _ in range(1, getrandbits(8))]
        field = Field('test', 'SInt64', 1)

        for n in numbers:
            self.assertEqual((n, b''), field.decode(0x08, field.encode(n)[1:]))

    def test_decode_encode_string(self):
        field = Field('test', 'String', 1)
        data = field.encode('test string')
        (tag, data) = field.get_tag(data)
        self.assertEqual(('test string', b''), field.decode(tag, data))

    def test_decode_encode_bytes(self):
        field = Field('test', 'Bytes', 1)
        data = field.encode(b'test string')
        (tag, data) = field.get_tag(data)
        self.assertEqual((b'test string', b''), field.decode(tag, data))
