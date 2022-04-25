PROTO = "tests/tests.proto"
OUTPUT = generated
INCLUDE = tests

FILES = ${OUTPUT} unittest.py protobuf tests

AMPY = $(shell which ampy) -p ${PORT}

PORT = /dev/cu.usbserial-*

.PHONY: full-tests tests test micro-deps micro-test clean proto test-dev test-data ${FILES}
	
test: test-3 micro-test

test-dev: proto test-data micro-test ${FILES}

${FILES}:
	${AMPY} put $@ $@

test-3: ${OUTPUT}/tests_upb2.py ${OUTPUT}/test_data_generated.py
	python3 -m unittest

micro-deps:
	micropython -m upip install -p . micropython-unittest

micro-test: micro-deps
	micropython -c 'import unittest; unittest.main("tests");'

test-data: ${OUTPUT}/test_data_generated.py


${OUTPUT}/test_data_generated.py: ${OUTPUT}/tests_pb2.py
	python3 -c 'from scripts.gen_test_data import main; main();'

proto: ${OUTPUT}/tests_upb2.py ${OUTPUT}/tests_pb2.py

${OUTPUT}/tests_upb2.py:
	protoc --plugin=protoc-gen-custom=scripts/uprotobuf_plugin.py \
         --custom_out=${OUTPUT} \
         -I${INCLUDE} \
         ${PROTO}

${OUTPUT}/tests_pb2.py:
	protoc --python_out=${OUTPUT} ${PROTO}
	mv ${OUTPUT}/tests/*_pb2.py ${OUTPUT}
	rm -rf ${OUTPUT}/tests

clean:
	rm -rf ${OUTPUT}/*_upb*.py
	rm -rf ${OUTPUT}/*_pb*.py
	rm -rf **/__pycache__
	rm -rf __pycache__
	rm -rf ${OUTPUT}/*_generated.py
	rm -rf unittest.py
