from google.protobuf.descriptor_pb2 import FieldDescriptorProto as FProto
from generated.tests_pb2 import Test1

VALUES = [
    0, 1, -1,
    127, -127, 128, -128,
    255, -255, 256, -256,
    65535, -65535, 65537, -65536
]

def create_value(val, field_type=FProto.TYPE_INT32):
    if field_type == FProto.TYPE_BOOL:
        return bool(val)

    elif field_type in (
            FProto.TYPE_INT32,
            FProto.TYPE_INT64,
            FProto.TYPE_SFIXED32,
            FProto.TYPE_SFIXED64,
            FProto.TYPE_SINT32,
            FProto.TYPE_SINT64):
        return val

    elif field_type in (
            FProto.TYPE_FIXED32,
            FProto.TYPE_FIXED64,
            FProto.TYPE_UINT32,
            FProto.TYPE_UINT64):
        return val if val >= 0 else None

    elif field_type == FProto.TYPE_ENUM:
        return val if val in Test1.Test1Enum.values() else None

    elif field_type == FProto.TYPE_BYTES:
        return "{}".format(val).encode('utf-8')

    elif field_type == FProto.TYPE_STRING:
        return "{}".format(val)

    elif field_type in (
            FProto.TYPE_DOUBLE,
            FProto.TYPE_FLOAT,
        ):
        return float(val)
    elif field_type == FProto.TYPE_MESSAGE:
        return None
       # TODO: Add correct generation for Message
       #  message = Test1.TestEmbed()
       #  message.Int32 = val
       #  return message

def main():
    fields = []
    with open('generated/test_data_generated.py', 'w') as f:
        print("TEST_DATA = [", file=f)
        for field in Test1.DESCRIPTOR.fields:
            fields.append(field.name)
            message = Test1()
            for val in VALUES:
                value = create_value(val, field.type)
                if value is not None and field.label != FProto.LABEL_REPEATED:
                    message.Clear()
                    if field.type == FProto.TYPE_MESSAGE:
                        getattr(message, field.name).CopyFrom(value)
                    else:
                        setattr(message, field.name, value)

                    print("{", file=f)
                    if type(value) == str:
                        print("'decoded': '{}',".format(value), file=f)
                    else:
                        print("'decoded': {},".format(value), file=f)
                    print("'name': '{}',\n'encoded': {},".format(field.name, message.SerializeToString()), file=f)
                    print("},", file=f)
                    
        print("]", file=f)
        print("FIELDS = {}".format(fields), file=f)
            

if __name__ == "__main__":
    main()
