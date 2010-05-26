import os.path, unittest
import aml
import file_utils

self_dir = os.path.dirname(__file__)
input_dir = os.path.join(self_dir, 'fixtures', 'input')
output_dir = os.path.join(self_dir, 'fixtures', 'output')

class TestAml(unittest.TestCase):
    def run_test(self, name):
        input = file_utils.read_file(os.path.join(input_dir, name + '.at'))
        actual_output = aml.convert_text(input)
        expected_output = file_utils.read_file(os.path.join(output_dir, name + '.jt'))
        self.assertEqual(actual_output, expected_output)
    
    def test_singleline_text(self):
        self.run_test('singleline-text')
    
    def test_multiline_text(self):
        self.run_test('multiline-text')

if __name__ == '__main__':
    unittest.main()
