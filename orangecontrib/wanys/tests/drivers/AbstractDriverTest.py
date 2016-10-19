"""
Test for abstract driver.
"""
import unittest
from orangecontrib.srw.util.OpticalElementSourceGaussian import OpticalElementSourceGaussian
from orangecontrib.srw.util.OpticalElementAperture import OpticalElementAperture
from orangecontrib.srw.util.OpticalElementLens import OpticalElementLens
from orangecontrib.srw.util.OpticalElementScreen import OpticalElementScreen
from orangecontrib.srw.util.OpticalElementSpace import OpticalElementSpace

from orangecontrib.srw.drivers.AbstractDriver import AbstractDriver
from orangecontrib.srw.tests.drivers.AbstractDriverDataTest import AbstractDriverDataMock

class AbstractDriverMock(AbstractDriver):

    def addToWavefront(self, optical_element, in_data, typename):
        wavefront = in_data.wavefront()
        wavefront = "%s - %s:%s" % (wavefront, typename, optical_element.name())
        
        out_data = self.createData()
        print(wavefront)
        out_data.setWavefront(wavefront)
        
        return out_data


    def hashInputData(self, optical_element, in_data):
        """
        Hashes the input data.
        """
        return hash(in_data.wavefront())

    def createData(self):
        """
        Factory method for driver data.
        """
        return AbstractDriverDataMock()

    def _calculateDataSource(self, optical_element, in_data):
        """
        Calculates output data from input data for a source.
        """
        in_data = self.createData()
        return self.addToWavefront(optical_element, in_data, "SOURCE")

    def _calculateDataSpace(self, optical_element, in_data):
        """
        Calculates output data from input data for a drift space.
        """
        return self.addToWavefront(optical_element, in_data, "SPACE")
    
    def _calculateDataApertureRectangle(self, optical_element, in_data):
        """
        Calculates output data from input data for a aperture.
        """
        return self.addToWavefront(optical_element, in_data, "APERATURE")
  
    
    def _calculateDataLens(self, optical_element, in_data):
        """
        Calculates output data from input data for a lens.
        """
        return self.addToWavefront(optical_element, in_data, "LENS")

    def _calculateDataScreen(self, optical_element, in_data):
        """
        Calculates output data from input data for a screen.
        """
        return self.addToWavefront(optical_element, in_data, "SCREEN")

class AbstractDriverTest(unittest.TestCase):
    def testConstructor(self):
        driver = AbstractDriverMock()
        
        self.assertIsInstance(driver, AbstractDriver)
        
    def testTravers(self):
        source = OpticalElementSourceGaussian("source")
        space_1 = OpticalElementSpace("space 1")
        aperture = OpticalElementAperture("aperature")
        space_2 = OpticalElementSpace("space 2")
        lens = OpticalElementLens("lens")
        space_3 = OpticalElementSpace("space 3")
        screen = OpticalElementScreen("screen")

        source.addOutput(space_1)
        space_1.addOutput(aperture)
        aperture.addOutput(space_2)
        space_2.addOutput(lens)
        lens.addOutput(space_3)
        space_3.addOutput(screen)
        
        driver = AbstractDriverMock()

        source.startTravers(driver)
        source.startTravers(driver)