"""
Abstract data for all optical simulation driver.
"""

class AbstractDriverData(object):
    def __init__(self):
        self.__input_hash = None
    
    def setInputHash(self, input_hash):
        """
        Sets the input hash.
        """
        self.__input_hash = input_hash
        
    def inputHash(self):
        """
        Gets the input hash.
        """        
        return self.__input_hash
    
