"""
Data for SRW driver.
"""
from orangecontrib.wanys.drivers.AbstractDriverData import AbstractDriverData

class SRWDriverData(AbstractDriverData):
    def __init__(self):
        AbstractDriverData.__init__(self)
        self.setWavefront(None)
        
    def setWavefront(self, wavefront):
        self.__wavefront = wavefront
    
    def wavefront(self):
        return self.__wavefront
