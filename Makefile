PROTO = "tests/tests.proto"
OUTPUT = generated
INCLUDE = tests

.PHONY: full-tests tests test micro-deps micro-test clean proto
	
full-tests: tests clean

tests: test micro-test

test: ${OUTPUT}/tests_upb2.py ${OUTPUT}/test_data_generated.py
	python3 -m unittest

micro-deps:
	micropython -m upip install -p . micropython-unittest

micro-test: micro-deps
	micropython -c 'import unittest; unittest.main("tests");'

${OUTPUT}/test_data_generated.py: ${OUTPUT}/tests_pb2.py
	python3 -c 'from scripts.gen_test_data import main; main();'

proto: clean ${OUTPUT}/tests_upb2.py ${OUTPUT}/tests_pb2.py

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
