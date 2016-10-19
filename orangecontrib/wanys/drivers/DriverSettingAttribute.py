"""
Represents a driver attribute. (e.g. number of rays, extension of wavefront,...)
"""

class DriverSettingAttribute(object):
    def __init__(self, name, description, attribute_type, default_value=None):
        self.__name = name
        self.__description = description
        self.__type = attribute_type
        self.__default_value = default_value
        
        self.setValue(self.defaultValue())
        
    def name(self):
        return self.__name
    
    def description(self):
        return self.__description
    
    def type(self):
        return self.__type
    
    def defaultValue(self):
        return self.__default_value
    
    def setValue(self, value):
        self.__value = value
    
    def value(self):
        return self.__value
        
        