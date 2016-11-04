"""
Tests driver settings attributes.
"""
import unittest
from orangecontrib.wanys.drivers.DriverSettingAttribute import DriverSettingAttribute

class DriverSettingAttributeTest(unittest.TestCase):
    def testConstructor(self):
        attribute_1 = DriverSettingAttribute("name","description", str)
        attribute_2 = DriverSettingAttribute("name","description", int,-2)
        
        self.assertEqual(attribute_1.name(), "name")        
        self.assertEqual(attribute_1.description(), "description")
        self.assertEqual(attribute_1.type(), str)
        self.assertEqual(attribute_1.defaultValue(), None)
        self.assertEqual(attribute_1.value(), None)

        self.assertEqual(attribute_2.type(), int)        
        self.assertEqual(attribute_2.defaultValue(), -2)
        self.assertEqual(attribute_2.value(), -2)
        
                        