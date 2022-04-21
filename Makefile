PROTO = "tests/tests.proto"
OUTPUT = tests
INCLUDE = tests


test: tests/tests_upb2.py tests/test_data_generated.py
	python3 -m unittest

tests/test_data_generated.py: tests/tests_pb2.py
	python3 -m tests.gen_test_data

proto: clean tests/tests_upb2.py tests/tests_pb2.py

tests/tests_upb2.py:
	protoc --plugin=protoc-gen-custom=protobuf/uprotobuf_plugin.py \
         --custom_out=${OUTPUT} \
         -I${INCLUDE} \
         ${PROTO}

tests/tests_pb2.py:
	protoc --python_out=. ${PROTO}

clean:
	rm -rf tests/*_upb2.py
	rm -rf tests/*_pb2.py
	rm -rf tests/__pycache__
