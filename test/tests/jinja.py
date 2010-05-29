import sys
import os.path, unittest
import shpaml_jinja
import file_utils

self_dir = os.path.dirname(__file__)
fixtures_dir = os.path.join(self_dir, '..', 'fixtures', 'jinja')
input_dir = os.path.join(fixtures_dir, 'input')
output_dir = os.path.join(fixtures_dir, 'output')

class TestAml(unittest.TestCase):
    def run_test(self, name):
        input = file_utils.read_file(os.path.join(input_dir, name + '.at'))
        actual_output = shpaml_jinja.convert_text(input)
        expected_output = file_utils.read_file(os.path.join(output_dir, name + '.jt'))
        self.assertEqual(actual_output, expected_output)
    
    def test_singleline_text(self):
        self.run_test('singleline-text')
    
    def test_multiline_text(self):
        self.run_test('multiline-text')

if __name__ == '__main__':
    unittest.main()