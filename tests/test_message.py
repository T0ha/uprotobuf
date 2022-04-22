import unittest
from .test_data_generated import *
from .tests_upb2 import Test1

class TestMessage(unittest.TestCase):
    def test_message_defaults(self):
        message = Test1()

        self._assertDefault(message)
        self.assertEqual(message.encode(), b'')

    def test_message_decode(self):
        for data in TEST_DATA:
            message = Test1.decode(data['encoded'])
            value = getattr(message, data['name'])

            self.assertEqual(value, data['decoded'], "{}".format(data['name']))
            self._assertDefault(message, exclude=[FIELDS.index(data['name'])])

    def test_message_all_fields_decode(self):
        encoded = b''
        checks = {}

        for data in TEST_DATA:
            encoded += data['encoded']
            checks[data['name']] = data['decoded']

        message = Test1.decode(encoded)

        for field, value in checks.items():
            decoded = getattr(message, field)
            self.assertEqual(decoded, value, "{}".format(field))
            

    def _assertDefault(self, message, exclude=[]):
        asserts = [
            lambda: self.assertEqual(message.Int32, 0),
            lambda: self.assertEqual(message.Sint32, 0),
            lambda: self.assertEqual(message.Uint32, 0),

            lambda: self.assertEqual(message.Int64, 0),
            lambda: self.assertEqual(message.Sint64, 0),
            lambda: self.assertEqual(message.Uint64, 0),

            lambda: self.assertEqual(message.Bool, False),

            lambda: self.assertEqual(message.Enum, Test1.Test1Enum.ValueA),

            lambda: self.assertEqual(message.Fixed32, 0),
            lambda: self.assertEqual(message.Fixed64, 0),
            lambda: self.assertEqual(message.Sfixed32, 0),
            lambda: self.assertEqual(message.Sfixed64, 0),
            lambda: self.assertEqual(message.Float, 0.0),
            lambda: self.assertEqual(message.Double, 0.0),

            lambda: self.assertEqual(message.String, ""),
            lambda: self.assertEqual(message.Bytes, b""),
            lambda: self.assertEqual(message.Message_, None),
            lambda: self.assertEqual(message.Repeated, []),
        ]

        for i in range(0, len(asserts)):
            if i not in exclude:
                asserts[i]()
