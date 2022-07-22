import unittest
from protobuf.uprotobuf import EnumValueError
from .test_data import *

class TestEnum(unittest.TestCase):
    def test_attributes(self):
        self.assertEqual(Enum1.one, 1)
        self.assertEqual(Enum1.two, 2)
        self.assertEqual(Enum1.three, 3)

    def test_default(self):
        self.assertEqual(Enum1.default, 1)
        
    def test_decode(self):
        self.assertEqual(Enum1.decode(2), 2)
        self.assertEqual(Enum1.decode(2), Enum1.two)

        with self.assertRaises(EnumValueError):
            Enum1.decode(5)
