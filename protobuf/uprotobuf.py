try:
    import ustruct as struct
except ImportError:
    import struct


ZigZagSubTypes = (
    'SInt32',
    'SInt64',
)

SignedSubTypes = (
    'Int32',
    'Int64',
)

VarintSubTypes = (
    'UInt32',
    'UInt64',
    'Bool',
    'Enum',
) + ZigZagSubTypes + SignedSubTypes

LengthSubTypes = (
    'String',
    'Message',
    'Group',
    'Bytes',
)

Fixed64SubTypes = (
    'Fixed64',
    'SignedFixed64',
    'Double',
)

Fixed32SubTypes = (
    'Fixed32',
    'SignedFixed32',
    'Float',
)

FixedSubTypes = Fixed32SubTypes + Fixed64SubTypes

AllowedSubTypes = VarintSubTypes + LengthSubTypes + FixedSubTypes

class FieldTagError(Exception):
    pass

class UnsupportedTypeError(Exception):
    pass

class FieldNotFound(Exception):
    pass

class Enum(dict):
    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        return self[name]

class Field(object):
    def __init__(self, name, type, id, repeated=False, required=False, default=None, **options):
        if type not in AllowedSubTypes:
            raise UnsupportedTypeError

        self.name = name
        self.type = type
        self.id = id
        self.repeated = repeated
        self.required = required
        self.options = options

        if type in ('Message', 'Enum'):
            self.cls = options['cls']

        if type == 'Float':
            self._fmt='<f'
        elif type == 'Double':
            self._fmt='<d'
        elif type  in Fixed32SubTypes:
            self._fmt="<i"
        elif type  in Fixed64SubTypes:
            self._fmt="<q"

        self._add_tag()
        self._add_default(default)

    @staticmethod
    def get_tag(data):
        return Field._decode_varint(data)

    def decode(self, tag, data):
        if tag != self.tag:
            raise FieldTagError

        if self.type in VarintSubTypes:
            (value, rest) = self._decode_varint(data)
            if self.type == 'Bool':
                value = bool(value)
            elif self.type in SignedSubTypes:
                value = self._to_signed(value)
            elif self.type in ZigZagSubTypes:
                value = self._decodeZigZag(value)

            return value, rest

        elif self.type in LengthSubTypes:
            (length, rest) = self._decode_varint(data)
            (value, rest) = rest[0: length], rest[length:]
            if self.type == 'String':
                return value.decode('utf-8'), rest
            elif self.type == 'Bytes':
                return value, rest
            elif self.type == 'Message':
                return self.cls.decode(value), rest
            else:
                raise UnsupportedTypeError

        elif self.type in Fixed64SubTypes:
            (value, rest) = data[0:8], data[8:]
            return struct.unpack(self._fmt, value)[0], rest
             
        elif self.type in Fixed32SubTypes:
            (value, rest) = data[0:4], data[4:]
            return struct.unpack(self._fmt, value)[0], rest

        else:
            raise UnsupportedTypeError

    def encode(self, value):
        if value == self.default:
            return b""

        if self.type in VarintSubTypes:
            if self.type in ZigZagSubTypes:
                value = self._encodeZigZag(value)
            data = self._encode_varint(value)

        elif self.type in LengthSubTypes:
            if self.type == 'String':
                data = value.encode('utf-8')
            elif self.type == 'Bytes':
                data = value
            elif self.type == 'Message':
                data = self.cls.encode(value)
            else:
                raise UnsupportedTypeError

            data = self._encode_varint(len(data)) + data

        elif self.type in FixedSubTypes:
            data = struct.pack(self._fmt, value)

        else:
            raise UnsupportedTypeError

        return bytes([self.tag]) + data

    @staticmethod
    def _decode_varint(data):
        binary = []
        i = 0
        while True:
            binary.append(data[i])
            if not data[i] & 0x80:
                break
            i += 1
        rest = data[i + 1:]

        value = 0
        for i, d in enumerate(binary):
            value |= (d & 0x7f) << (i * 7)

        return (value, rest)

    def _encode_varint(self, integer):
        val = []
        while integer != 0:
            val.append(integer & 0x7f | 0x80)
            integer >>= 7 
        
        if val == []:
            return b'\x00'

        val[-1] ^= 0x80
        return bytes(val)
        
    def _encodeZigZag(self, n, bits=32):
        return (n<<1)^(n>>(bits-1))

    def _decodeZigZag(self, n):
        return (n >> 1) ^- (n & 1)

    def _add_tag(self):
        self.tag = self.id << 3
        if self.type in Fixed64SubTypes:
            self.tag += 1
        elif self.type in Fixed32SubTypes:
            self.tag += 5
        elif self.type in LengthSubTypes:
            self.tag += 2

    def _add_default(self, default):
        if default is not None:
            self.default = default
        elif self.repeated:
            self.default = []
        elif self.type in ('Float', 'Double'):
            self.default = 0.0
        elif self.type == 'Enum':
            self.default = self.cls.__dict__.values()
        elif self.type in VarintSubTypes + FixedSubTypes:
            self.default = 0
        elif self.type == 'String':
            self.default = ""
        elif self.type == 'Bytes':
            self.default = b""
        elif self.type == 'Bool':
            self.default = False
        else:
            self.default = None

    def _to_signed(self, value):
        if self.type == 'Int32':
            bitLength = 32
        else:
            bitLength = 64

        mask = (2 ** bitLength) - 1
        if value & (1 << (bitLength - 1)):
            return value | ~mask
        else:
            return value & mask
    

class Message(object):
    _fields = []
    _fields_by_tag = {}
    _initiated = False

    def __init__(self):
        for field in self._fields:
            self._fields_by_tag[field.tag] =  field
            setattr(self, field.name, field.default)
        self._initiated = True

    @classmethod
    def decode(cls, data):
        msg = cls()
        msg.merge_encoded(data)
        return msg

    def encode(self):
        data = b''
        for field in self._fields:
            data += field.encode(self.__dict__[field.name])
        return data

    def merge(self, msg):
        # TODO: refactor for efficiency
        self.merge_encoded(msg.encode())

    def merge_encoded(self, data):
        rest = data
        while rest != b'':
            (tag, rest) = Field.get_tag(rest)
            field = self._fields_by_tag[tag]
            (value, rest) = field.decode(tag, rest)
            if field.repeated:
                self.__dict__[field.name].append(value)
            else:
                setattr(self, field.name, value)

    def __repr__(self):
        return str(self.__dict__)

   # def __setattr__(self, name, value):
   #     if self._initiated and name not in self.__dict__:
   #         raise FieldNotFound(name)
   #     else:
   #         setattr(self, name, value)
