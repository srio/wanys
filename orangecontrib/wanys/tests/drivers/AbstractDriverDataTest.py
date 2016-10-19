"""
Test for abstract driver data.
"""
import unittest
from orangecontrib.srw.drivers.AbstractDriverData import AbstractDriverData

class AbstractDriverDataMock(AbstractDriverData):
    def __init__(self):
        AbstractDriverData.__init__(self)
        self.setWavefront(None)
        
    def setWavefront(self, wavefront):
        self.__wavefront = wavefront
    
    def wavefront(self):
        return self.__wavefront

class AbstractDriverDataTest(unittest.TestCase):
    def testConstructor(self):
        return
