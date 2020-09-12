import os
import sys
import unittest
from subprocess import Popen, PIPE


class TestConnectZ(unittest.TestCase):
    def test_algorithm(self):
        print('Running test suite...')
        with open('test_suite/targets', 'r') as test_file:
            for test_info in test_file.readlines():
                test_number, target = test_info.split()
                process = Popen(['python', 'connectz.py', f'test_suite/test{test_number}'], stdout=PIPE)
                stdout  = process.communicate()
                self.assertEqual(int(stdout[0]), int(target))

                
if __name__ == '__main__':
    unittest.main()