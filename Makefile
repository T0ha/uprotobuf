PROTO = "tests/tests.proto"
OUTPUT = tests
INCLUDE = tests


test: tests/tests_upb2.py
	python -m unittest

proto: clean tests/tests_upb2.py

tests/tests_upb2.py:
	protoc --plugin=protoc-gen-custom=protobuf/uprotobuf_plugin.py \
         --custom_out=${OUTPUT} \
         -I${INCLUDE} \
         ${PROTO}

clean:
	rm -rf tests/*_upb2.py
