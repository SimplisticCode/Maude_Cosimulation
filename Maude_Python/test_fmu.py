import unittest
from unittest import result

from maude_load import *

class TestMaude(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_encodeInput(self):
        port = Input("1", "real", "InputTest", 'reactive')
        actual = port.encode().replace(" ", "")
        expected = '< "InputTest" : Input | contract : reactive, value : < 1 >, type : real, time : 0, status : Undef >'.replace(" ", "")
        print(result)
        self.assertEqual(actual, expected)
    
    def test_encodeOutput(self):
        port = OutputPort("1", "real", "OutputTest", "{port1, port2}")
        actual = port.encode().replace(" ", "")
        expected = '< "OutputTest" : Output | dependsOn : {port1, port2}, value : < 1 >, type : real, time : 0, status : Undef >'.replace(" ", "")
        self.assertEqual(actual, expected)


    def test_parseInput(self):
        port = Input("0", "integer", "valveState", 'reactive')
        expr = portModule.parseTerm('< "valveState" : Input | value : < 0 >, type : integer, time : 0, contract : reactive, status : Undef >')
        self.assertEqual(str(expr.getSort()), 'Object')
        parsed = port.encode()
        print(parsed)
        ans = portModule.parseTerm(parsed)
        self.assertEqual(str(ans.getSort()), 'Object')

    def test_parseOutput(self):
        port = OutputPort("1", "real", "OutputTest", "empty")
        encoded = port.encode()
        ans = portModule.parseTerm(encoded)
        expr = portModule.parseTerm('< "fk" : Output | time : 0, status : Undef, dependsOn : empty >')
        self.assertEqual(str(expr.getSort()), 'Object')
    

if __name__ == '__main__':
    unittest.main()
