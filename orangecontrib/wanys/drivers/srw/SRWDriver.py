from srwlib import *
import numpy as np
import copy

from orangecontrib.wanys.drivers.AbstractDriver import AbstractDriver
from orangecontrib.wanys.drivers.srw.SRWDriverData import SRWDriverData
from orangecontrib.wanys.drivers.DriverSettingAttribute import DriverSettingAttribute
from orangecontrib.wanys.drivers.DriverSettings import DriverSettings
from orangecontrib.wanys.drivers.srw.SRWAdapter import SRWAdapter

from orangecontrib.wanys.util.Polarization import LinearVertical, LinearHorizontal
from orangecontrib.wanys.BeamlineComponents.Beam.ElectronBeam import ElectronBeam
from orangecontrib.wanys.BeamlineComponents.Source.SourceGaussian import SourceGaussian
from orangecontrib.wanys.BeamlineComponents.Source.Undulator import Undulator

class SRWDriver(AbstractDriver):
    
    def __init__(self):
        self.srw_wavefront = None

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
        return SRWDriverData()

    def _calculateDataElectronBeam(self, electron_beam, in_data):
        """
        Calculates output data from input data for a source.
        """
        out_data = self.createData()
        out_data.setWavefront(electron_beam)
        print(out_data.wavefront())
        return out_data

    def _calculateDataUndulator(self, undulator, in_data):
        """
        Calculates output data from input data for a source.
        """
        print(in_data.wavefront())
        if not isinstance(in_data.wavefront(), ElectronBeam):
             raise Exception("SRW undulator expects electron beam as in_data. Got %s"%str(in_data.wavefront()))
        # TODO: FIX!!!
        adapter = SRWAdapter()
        electron_beam = in_data.wavefront()
        # TODO: FIX!!!
        driver_settings = undulator._optical_element.driverSettings()
        z_start = driver_settings.valueByName("Distance to first optical element")
        first_aperture = driver_settings.valueByName("Rectangular aperture at first optical element")


        srw_electron_beam = adapter.electronBeam(electron_beam)

        magFldCnt = adapter.magnetFieldFromUndulator(undulator)

        max_theta = undulator.gaussianCentralConeDivergence(electron_beam.gamma()) * 2.5
        print("GAUSSION ESTIMATE BEAM SIZE", max_theta)

        grid_length = max_theta * z_start / sqrt(2.0)
        wfr = adapter.createQuadraticSRWWavefrontSingleEnergy(grid_size=1000,
                                                              grid_length=grid_length,
                                                              z_start=z_start,
                                                              electron_beam=electron_beam,
                                                              energy=int(undulator.resonanceEnergy(electron_beam.gamma(),0.0,0.0)))


        precision_parameter = adapter.normalPrecisionParameter()

        srwl.CalcElecFieldSR(wfr, 0, magFldCnt, precision_parameter)

        out_data = self.createData()
        out_data.setWavefront(wfr)
        return out_data

    def _calculateDataSourceGaussian(self, source_gaussian, in_data):
        """
        Calculates output data from input data for a Gaussian source.
        """
        adapter = SRWAdapter()
        # TODO: FIX!!!
        driver_settings = source_gaussian._optical_element.driverSettings()
        distance_first_element = driver_settings.valueByName("Distance to first optical element")
        first_aperture = driver_settings.valueByName("Rectangular aperture at first optical element")

        # TODO: FIX!!!
        electron_beam = ElectronBeam(source_gaussian.energy(),0.0,0.2, 1)
        srw_wavefront = adapter.createSRWWavefrontFromSourceGaussian(electron_beam=electron_beam,
                                                                     source_gaussian=source_gaussian,
                                                                     distance_first_element=distance_first_element,
                                                                     first_aperture=first_aperture)

        out_data = self.createData()
        out_data.setWavefront(srw_wavefront)
        return out_data

    def propagateWavefront(self, beamline_component, in_data, srw_optical_element):
        driver_settings = beamline_component._optical_element.driverSettings()
        
        if driver_settings is None:
            print("%s uses default settings" % beamline_component)
            driver_settings = self.driverSettings(None)
        
        srw_preferences = self._driverSettingsToSRWParameters(driver_settings)
        

        optical_beamline=SRWLOptC([srw_optical_element],
                                  [srw_preferences])
        
#        wavefront = in_data.wavefront()#copy.deepcopy(in_data.wavefront())
        print("Using high mem usage wavefront deep copy")
        wavefront = copy.deepcopy(in_data.wavefront())

        print("SRW begin propagation", srw_optical_element)
        srwl.PropagElecField(wavefront, optical_beamline)
        print("SRW end propagation", srw_optical_element)
        print("SRW RADI", wavefront.Rx, wavefront.Ry, wavefront.dRx, wavefront.dRy)

        out_data = self.createData()
        out_data.setWavefront(wavefront)
        return out_data

    def _calculateDataDriftSpace(self, beamline_component, in_data):
        """
        Calculates output data from input data for a drift space.
        """
        srw_drift_space = SRWLOptD(beamline_component.length())
        result = self.propagateWavefront(beamline_component, in_data, srw_drift_space)
        return result

    def _calculateDataApertureCircle(self, beamline_component, in_data):
        """
        Calculates output data from input data for a circular aperture.
        """
        print("diameter",beamline_component.diameter())
        srw_aperture = SRWLOptA('c', 'a',
                                beamline_component.diameter(),
                                beamline_component.diameter())

        result = self.propagateWavefront(beamline_component, in_data, srw_aperture)
        return result
    
    def _calculateDataApertureRectangle(self, beamline_component, in_data):
        """
        Calculates output data from input data for a rectangular aperture.
        """
        
        srw_aperture = SRWLOptA('r', 'a',
                                beamline_component.lengthHorizontal(),
                                beamline_component.lengthVertical())

        result = self.propagateWavefront(beamline_component, in_data, srw_aperture)
        return result  
    
    def _calculateDataLensIdeal(self, beamline_component, in_data):
        """
        Calculates output data from input data for a lens.
        """
        srw_lens = SRWLOptL(beamline_component.focalX(),
                            beamline_component.focalY())
        result = self.propagateWavefront(beamline_component,in_data, srw_lens)
        return result
    
    def _calculateDataScreen(self, beamline_component, in_data):
        """
        Calculates output data from input data for a screen.
        """
        return copy.deepcopy(in_data)
    
    def driverSettings(self, beamline_component):
        #***********Wavefront Propagation Parameters:
        #[0]: Auto-Resize (1) or not (0) Before propagation
        #[1]: Auto-Resize (1) or not (0) After propagation
        #[2]: Relative Precision for propagation with Auto-Resizing (1. is nominal)
        #[3]: Allow (1) or not (0) for semi-analytical treatment of the quadratic (leading) phase terms at the propagation
        #[4]: Do any Resizing on Fourier side, using FFT, (1) or not (0)
        #[5]: Horizontal Range modification factor at Resizing (1. means no modification)
        #[6]: Horizontal Resolution modification factor at Resizing
        #[7]: Vertical Range modification factor at Resizing
        #[8]: Vertical Resolution modification factor at Resizing
        #[9]: Type of wavefront Shift before Resizing (not yet implemented)
        #[10]: New Horizontal wavefront Center position after Shift (not yet implemented)
        #[11]: New Vertical wavefront Center position after Shift (not yet implemented)

        attributes = [
            DriverSettingAttribute("Auto resize before propagation",
                                   "Auto resize before propagation",
                                   bool,
                                   False),
            DriverSettingAttribute("Auto resize after propagation",
                                   "Auto resize after propagation",
                                   bool,
                                   False),
            DriverSettingAttribute("Relative precision for auto resize",
                                   "Relative Precision for propagation with Auto-Resizing (1. is nominal)",
                                   float,
                                   1.0),
            DriverSettingAttribute("Semi-analytical treatment of leading phase",
                                   "Allow (1) or not (0) for semi-analytical treatment of the quadratic (leading) phase terms at the propagation",
                                   bool,
                                   True),
            DriverSettingAttribute("Resize using FFT",
                                   "Do any Resizing on Fourier side, using FFT",
                                   bool,
                                   False),
            DriverSettingAttribute("Horizontal scaling",
                                   "Horizontal Range modification factor at Resizing (1. means no modification)",
                                   float,
                                   1.0),
            DriverSettingAttribute("Horizontal resolution",
                                   "Horizontal Resolution modification factor at Resizing",
                                   float,
                                   1.0),
            DriverSettingAttribute("Vertical scaling",
                                   "Vertical Range modification factor at Resizing (1. means no modification)",
                                   float,
                                   1.0),
            DriverSettingAttribute("Vertical resolution",
                                   "Vertical Resolution modification factor at Resizing",
                                   float,
                                   1.0),
            DriverSettingAttribute("Type of wavefront Shift",
                                   "Type of wavefront Shift before Resizing (not yet implemented)",
                                   int,
                                   0),
            DriverSettingAttribute("New Horizontal wavefront Center",
                                   "New Horizontal wavefront Center position after Shift (not yet implemented)",
                                   int,
                                   0),
            DriverSettingAttribute("New Vertical wavefront Center",
                                   "New Vertical wavefront Center position after Shift (not yet implemented)",
                                   int,
                                   0),
                      ]                      

        print(beamline_component)
        if beamline_component is not None:
            print(beamline_component)
            if(isinstance(beamline_component, (Undulator, SourceGaussian))):
                attributes+=[
                DriverSettingAttribute("Distance to first optical element",
                                       "Distance to first optical element in m",
                                       float,
                                       10.0),
                DriverSettingAttribute("Rectangular aperture at first optical element",
                                       "Rectangular aperture at first optical element in m",
                                       float,
                                       0.0005)]


        return DriverSettings(self, attributes)
            
    def _driverSettingsToSRWParameters(self, driver_settings):
        
        result = []
        for name in self.driverSettings(None).names():
            value = driver_settings.valueByName(name)
            
            if type(value) is bool:
                value = int(value)
            
            result.append(value)

        return result

    def calculateIntensity3D(self, in_data):
        """
        Calculates 3D intensity distribution.
        """
        wfr = in_data.wavefront()
        mesh3 = deepcopy(wfr.mesh)
        arI3 = array('f', [0]*mesh3.nx*mesh3.ny) #"flat" array to take 2D intensity data
        srwl.CalcIntFromElecField(arI3, wfr, 6, 0, 3, mesh3.eStart, 0, 0) #extracts intensity
        plotMesh3x = [1e+06*mesh3.xStart, 1e+06*mesh3.xFin, mesh3.nx]
        plotMesh3y = [1e+06*mesh3.yStart, 1e+06*mesh3.yFin, mesh3.ny]
        print("SRW intensity")
        return [arI3, plotMesh3x, plotMesh3y]

    def calculateIntensityHorizontalCut(self, in_data, horizontal_coordinate):
        """
        Calculates a horizontal intensity cut.
        """
        wfr = in_data.wavefront()
        mesh = deepcopy(wfr.mesh)
        arI1x = array('f', [0]*mesh.nx) #array to take 1D intensity data (vs X)
        srwl.CalcIntFromElecField(arI1x, wfr, 6, 0, 1, mesh.eStart, 0, 0)
        plot_mesh = np.linspace(mesh.xStart, mesh.xFin, mesh.nx) *  10**6
        return [plot_mesh, arI1x]

    def calculateIntensityVerticalCut(self, in_data, vertical_coordinate):
        """
        Calculates a vertical intensity cut.
        """
        wfr = in_data.wavefront()
        mesh = deepcopy(wfr.mesh)
        arI1y = array('f', [0]*mesh.ny) #array to take 1D intensity data (vs Y)
        srwl.CalcIntFromElecField(arI1y, wfr, 6, 0, 2, mesh.eStart, 0, 0)
        plot_mesh = np.linspace(mesh.yStart, mesh.yFin, mesh.ny) * 10**6
        return [plot_mesh, arI1y]

    def calculatePhase3D(self, in_data):
        """
        Calculates 3D phase distribution.
        """        
        wfr = in_data.wavefront()
        mesh3 = deepcopy(wfr.mesh)

        arP3 = array('d', [0]*mesh3.nx*mesh3.ny) #"flat" array to take 2D phase data (note it should be 'd')
        srwl.CalcIntFromElecField(arP3, wfr, 0, 4, 3, mesh3.eStart, 0, 0) #extracts radiation phase
        plotMesh3x = [1e+06*mesh3.xStart, 1e+06*mesh3.xFin, mesh3.nx]
        plotMesh3y = [1e+06*mesh3.yStart, 1e+06*mesh3.yFin, mesh3.ny]
        
        return [arP3, plotMesh3x, plotMesh3y]
