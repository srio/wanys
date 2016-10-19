from orangecontrib.wanys.drivers.AbstractDriver import AbstractDriver
from orangecontrib.wanys.drivers.shadow.ShadowDriverData import ShadowDriverData
from orangecontrib.wanys.drivers.shadow.ShadowAdapter import ShadowAdapter
from orangecontrib.wanys.drivers.DriverSettingAttribute import DriverSettingAttribute
from orangecontrib.wanys.drivers.DriverSettings import DriverSettings

import Shadow


class ShadowDriver(AbstractDriver):
    
    def __init__(self):
        self.shadow_beam = None

    def hashInputData(self, optical_element, in_data):
        """
        Hashes the input data.
        """
        return hash(in_data.beam())

    def createData(self):
        """
        Factory method for driver data.
        """
        return ShadowDriverData()

    def _calculateDataSourceGaussian(self, source_gaussian, in_data):
        """
        Calculates output data from input data for a Gaussian source.
        """
        adapter = ShadowAdapter()

        source = adapter.shadowSourceFromSourceGaussian(source_gaussian)

        # TODO: FIX!!!
        source.NPOINT = source_gaussian._optical_element.driverSettings().valueByName("Number of rays")

        beam = Shadow.Beam()
        beam.genSource(source)

        out_data = self.createData()
        out_data.setBeam(beam)
        return out_data

    def _calculateDataScreen(self, beamline_component, in_data):
        """
        Calculates output data from input data for a screen.
        """

        return in_data
    
    def driverSettings(self, beamline_component):

        attributes = [
            DriverSettingAttribute("Semi-analytical treatment of leading phase",
                                   "Allow (1) or not (0) for semi-analytical treatment of the quadratic (leading) phase terms at the propagation",
                                   bool,
                                   True),
            DriverSettingAttribute("Vertical resolution",
                                   "Vertical Resolution modification factor at Resizing",
                                   float,
                                   1.0),
            DriverSettingAttribute("Number of rays",
                                   "the number of rays that are traced by shadows.",
                                   int,
                                   5000),
                      ]                      
        return DriverSettings(self, attributes)

    def calculateIntensity3D(self, in_data):
        """
        Calculates 3D intensity distribution.
        """
        beam = in_data.beam()

        adapter = ShadowAdapter()

        intensity = adapter.intensityFromBeam(beam)

        return intensity
        
    def calculatePhase3D(self, in_data):
        """
        Calculates 3D phase distribution.
        """        
        beam = in_data.beam()

        adapter = ShadowAdapter()

        phase = adapter.phaseFromBeam(beam)

        return phase
