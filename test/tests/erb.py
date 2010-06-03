import os.path, unittest
import aml_erb
import file_utils

self_dir = os.path.dirname(__file__)
input_dir = os.path.join(self_dir, '..', 'fixtures', 'erb', 'input')
output_dir = os.path.join(self_dir, '..', 'fixtures', 'erb', 'output')

class TestAml(unittest.TestCase):
    def run_test(self, name):
        input = file_utils.read_file(os.path.join(input_dir, name + '.erb.shpaml'))
        actual_output = aml_erb.convert_text(input)
        expected_output = file_utils.read_file(os.path.join(output_dir, name + '.erb'))
        self.assertEqual(actual_output, expected_output)
    
    def test_conditional(self):
        self.run_test('conditional')
    
    def test_loop(self):
        self.run_test('loop')
    
    def test_self_closing_block(self):
        self.run_test('self_closing_block')

if __name__ == '__main__':
    unittest.main()
