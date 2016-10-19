"""
Data for SRW driver.
"""
from orangecontrib.srw.drivers.AbstractDriverData import AbstractDriverData

import Shadow

class ShadowDriverData(AbstractDriverData):
    def __init__(self):
        AbstractDriverData.__init__(self)
        self.setBeam(None)
        
    def setBeam(self, beam):
        self._beam = beam
    
    def beam(self):
        return self._beam
