import os.path
import aml

self_dir = os.path.dirname(__file__)
input_dir = os.path.join(self_dir, 'fixtures', 'input')
output_dir = os.path.join(self_dir, 'fixtures', 'output')

tests = ['singleline-text', 'multiline-text']

def read_file(path):
    file = open(path)
    try:
        return file.read()
    finally:
        file.close()

for test in tests:
    input = read_file(os.path.join(input_dir, test + '.at'))
    actual_output = aml.convert_text(input)
    expected_output = read_file(os.path.join(output_dir, test + '.jt'))
    #print actual_output
    #print expected_output
    assert actual_output == expected_output
