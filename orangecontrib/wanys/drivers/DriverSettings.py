"""
Represents driver settings. (collection of driver attributes)
"""
import copy
import pickle
from collections import OrderedDict

class DriverSettings(object):
    def __init__(self, driver, list_driver_attributes):
        self._setDriver(driver)
        attributes = copy.deepcopy(list_driver_attributes)
        self.__attribute_dict = OrderedDict()
        
        for attribute in attributes:
            self.__attribute_dict[attribute.name()] = attribute
        
    def names(self):
        names = [attribute.name() for attribute in self.__attribute_dict.values()]
        return names
    
    def hasAttribute(self, name):
        return name in self.names()
    
    def _attributeByName(self, name):
        return self.__attribute_dict[name]

    def descriptionByName(self, name):
        attribute = self._attributeByName(name)
        return attribute.description()
    
    def typeByName(self, name):
        attribute = self._attributeByName(name)
        return attribute.type()

    def defaultValueByName(self, name):
        attribute = self._attributeByName(name)
        return attribute.defaultValue()

    def setValueByName(self, name, value):
        attribute = self._attributeByName(name)
        return attribute.setValue(value)

    def valueByName(self, name):
        attribute = self._attributeByName(name)
        return attribute.value()

    def saveAsString(self):
        return pickle.dumps(self)

    def _setDriver(self, driver):
        self._driver = driver

    def driver(self):
        return self._driver

    def isDriver(self, driver):

        try:
            is_driver = isinstance(self._driver, type(driver))
        except:
            is_driver = False

        return is_driver

    @staticmethod
    def loadFromString(as_string):
        return pickle.loads(as_string)
    
    def print(self):
        for name in self.names():
            print("%s%s%s" %(name,
                             self.typeByName(name),
                             str(self.valueByName(name))))
