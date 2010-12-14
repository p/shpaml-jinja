import os.path, unittest
import aml_erb
import file_utils

self_dir = os.path.dirname(__file__)
input_dir = os.path.join(self_dir, '..', 'fixtures', 'erubis', 'input')
output_dir = os.path.join(self_dir, '..', 'fixtures', 'erubis', 'output')

class TestAml(unittest.TestCase):
    def run_test(self, name):
        input = file_utils.read_file(os.path.join(input_dir, name + '.erb.shpaml'))
        actual_output = aml_erb.convert_text(input)
        expected_output = file_utils.read_file(os.path.join(output_dir, name + '.erb'))
        self.assertEqual(expected_output, actual_output)
    
    def test_preprocessed_expression(self):
        self.run_test('preprocessed_expression')
    
    def test_preprocessed_statement(self):
        self.run_test('preprocessed_statement')
    
    def test_preprocessed_if_else(self):
        self.run_test('preprocessed_if_else')

if __name__ == '__main__':
    unittest.main()
