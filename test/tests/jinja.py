import sys
import os.path, unittest
import aml_jinja
import file_utils

self_dir = os.path.dirname(__file__)
fixtures_dir = os.path.join(self_dir, '..', 'fixtures', 'jinja')
input_dir = os.path.join(fixtures_dir, 'input')
output_dir = os.path.join(fixtures_dir, 'output')

class TestAml(unittest.TestCase):
    def run_test(self, name):
        input = file_utils.read_file(os.path.join(input_dir, name + '.at'))
        actual_output = aml_jinja.convert_text(input)
        expected_output = file_utils.read_file(os.path.join(output_dir, name + '.jt'))
        self.assertEqual(expected_output, actual_output)
    
    def test_singleline_text(self):
        self.run_test('singleline_text')
    
    def test_multiline_text(self):
        self.run_test('multiline_text')
    
    def test_conditional(self):
        self.run_test('conditional')
    
    def test_elif(self):
        self.run_test('elif')
    
    def test_elif_else(self):
        self.run_test('elif_else')
    
    def test_multi_elif(self):
        self.run_test('multi_elif')
    
    def test_self_closing_tag(self):
        self.run_test('self_closing_tag')
    
    def test_line_continuation(self):
        self.run_test('line_continuation')

if __name__ == '__main__':
    unittest.main()
