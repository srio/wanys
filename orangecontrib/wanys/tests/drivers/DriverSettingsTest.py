"""
Represents driver settings. (collection of driver attributes)
"""
import unittest
from orangecontrib.wanys.drivers.DriverSettings import DriverSettings
from orangecontrib.wanys.drivers.DriverSettingAttribute import DriverSettingAttribute

class DriverSettingsTest(unittest.TestCase):
    def testConstructor(self):
        attribute = DriverSettingAttribute("attribute1", "an attribute", str)
        
        settings = DriverSettings([attribute])
        self.assertIsInstance(settings, DriverSettings)
        
    def testNames(self):
        attribute1 = DriverSettingAttribute("attribute1", "an attribute", str)
        attribute2 = DriverSettingAttribute("attribute2", "an attribute", int)
        
        settings = DriverSettings([attribute1, attribute2])
        
        names = settings.names()
        self.assertEqual(names[0], "attribute1")
        self.assertEqual(names[1], "attribute2")
        
    def testHasAttribute(self):
        attribute1 = DriverSettingAttribute("attribute1", "an attribute", str)
        attribute2 = DriverSettingAttribute("attribute2", "an attribute", int)
        
        settings = DriverSettings([attribute1, attribute2])
        
        self.assertTrue(settings.hasAttribute("attribute1"))
        self.assertTrue(settings.hasAttribute("attribute2"))
        self.assertFalse(settings.hasAttribute("attribute3"))
    
    def testAttributeByName(self):
        attribute1 = DriverSettingAttribute("attribute1", "an attribute", str)
        attribute2 = DriverSettingAttribute("attribute2", "an attribute", int)
        
        settings = DriverSettings([attribute1, attribute2])
        
        attribute = settings._attributeByName("attribute2")
        self.assertEqual(attribute.type(), int)

    def testDescriptionByName(self):
        attribute1 = DriverSettingAttribute("attribute1", "an attribute1", str)
        attribute2 = DriverSettingAttribute("attribute2", "an attribute2", int)
        
        settings = DriverSettings([attribute1, attribute2])
        
        description = settings.descriptionByName("attribute2")
        self.assertEqual(description, "an attribute2")
    
    def testTypeByName(self):
        attribute1 = DriverSettingAttribute("attribute1", "an attribute1", str)
        attribute2 = DriverSettingAttribute("attribute2", "an attribute2", int)
        
        settings = DriverSettings([attribute1, attribute2])
        
        a_type = settings.typeByName("attribute2")
        self.assertEqual(a_type, int)

    def testDefaultValueByName(self):
        attribute1 = DriverSettingAttribute("attribute1", "an attribute1", str, "abc")
        attribute2 = DriverSettingAttribute("attribute2", "an attribute2", int)
        
        settings = DriverSettings([attribute1, attribute2])
        
        default_value = settings.defaultValueByName("attribute1")
        self.assertEqual(default_value, "abc")
        default_value = settings.defaultValueByName("attribute2")
        self.assertEqual(default_value, None)

    def testSetAndGetValueByName(self):
        attribute1 = DriverSettingAttribute("attribute1", "an attribute1", str, "abc")
        attribute2 = DriverSettingAttribute("attribute2", "an attribute2", int)
        
        settings = DriverSettings([attribute1, attribute2])
        
        default_value = settings.setValueByName("attribute1","DEF")
        value = settings.valueByName("attribute1")
        
        self.assertEqual(value, "DEF")

    def testSaveAndLoadAsString(self):
        attribute1 = DriverSettingAttribute("attribute1", "an attribute1", str, "abc")
        attribute2 = DriverSettingAttribute("attribute2", "an attribute2", int)
        
        settings = DriverSettings([attribute1, attribute2])

        serialized = settings.saveAsString()
        clone = DriverSettings.loadFromString(serialized)
        
        self.assertEqual(settings.names(),
                         clone.names())
