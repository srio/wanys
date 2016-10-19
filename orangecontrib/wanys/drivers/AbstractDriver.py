"""
Abstract driver for all optical simulation software backend.
"""
from orangecontrib.wanys.util.OpticalElementScreen import OpticalElementScreen

from BeamlineComponents.Aperture.ApertureEllipse import ApertureEllipse
from BeamlineComponents.Aperture.ApertureCircle import ApertureCircle
from BeamlineComponents.Aperture.ApertureRectangle import ApertureRectangle
from BeamlineComponents.Aperture.ApertureSquare import ApertureSquare

from BeamlineComponents.DriftSpace.DriftSpace import DriftSpace

from BeamlineComponents.Lens.LensIdeal import LensIdeal

from BeamlineComponents.Beam.ElectronBeam import ElectronBeam

from BeamlineComponents.Source.SourceGaussian import SourceGaussian
from BeamlineComponents.Source.SourcePoint import SourcePoint
from BeamlineComponents.Source.Undulator import Undulator
from BeamlineComponents.Source.Wiggler import Wiggler

from BeamlineComponents.Stop.StopEllipse import StopEllipse
from BeamlineComponents.Stop.StopCircle import StopCircle
from BeamlineComponents.Stop.StopRectangle import StopRectangle
from BeamlineComponents.Stop.StopSquare import StopSquare


class AbstractDriver(object):
    def isDataUpToDate(self, optical_element, in_data, stored_data):
        if stored_data.inputHash() is None:
            return False
        
        is_up_to_date = (self.hashInputData(optical_element, in_data) == stored_data.inputHash())
        return is_up_to_date
    
    def hashInputData(self, optical_element, in_data):
        """
        Hashes the input data.
        """
        #raise Exception("Needs reimplementation")
        return None        

    def createData(self):
        """
        Factory method for driver data.
        """
        raise Exception("Needs reimplementation")
  
    def calculateData(self, optical_element, in_data):
        """
        Calculates output data from input data.
        """
        output_data = self._calculateData(optical_element, in_data)
        
        if in_data is not None:
            input_hash = self.hashInputData(optical_element, in_data)
        else:
            input_hash = None
            
        output_data.setInputHash(input_hash)
        return output_data

    def _calculateData(self, optical_element, in_data):
        """
        Calculates output data from input data.
        """
        print("Calculating: %s:%s" % (optical_element.elementTypename(),
                                      optical_element.name()))

        beamline_component = optical_element.beamlineComponent()

        # TODO: FIX!!!
        if beamline_component is not None:
            beamline_component._optical_element = optical_element

        out_data = None

        # Apertures
        if isinstance(beamline_component, ApertureCircle):
            out_data = self._calculateDataApertureCircle(beamline_component, in_data)
        elif isinstance(beamline_component,ApertureEllipse):
            out_data = self._calculateDataApertureEllipse(beamline_component, in_data)
        elif isinstance(beamline_component, ApertureRectangle):
            out_data = self._calculateDataApertureRectangle(beamline_component, in_data)
        elif isinstance(beamline_component, ApertureSquare):
            out_data = self._calculateDataApertureSquare(beamline_component, in_data)

        # DriftSpace
        if isinstance(beamline_component, DriftSpace):
            out_data = self._calculateDataDriftSpace(beamline_component, in_data)

        # Lens
        if isinstance(beamline_component, LensIdeal):
            out_data = self._calculateDataLensIdeal(beamline_component, in_data)

        # ElectronBeam
        if isinstance(beamline_component, ElectronBeam):
            out_data = self._calculateDataElectronBeam(beamline_component, in_data)

        # Source
        if isinstance(beamline_component, SourceGaussian):
            out_data = self._calculateDataSourceGaussian(beamline_component, in_data)
        elif isinstance(beamline_component, SourcePoint):
            out_data = self._calculateDataSourcePoint(beamline_component, in_data)
        elif isinstance(beamline_component,Undulator):
            out_data = self._calculateDataUndulator(beamline_component, in_data)
        elif isinstance(beamline_component,Wiggler):
            out_data = self._calculateDataWiggler(beamline_component, in_data)

        # Stop
        if isinstance(beamline_component, StopCircle):
            out_data = self._calculateDataStopCircle(beamline_component, in_data)
        elif isinstance(beamline_component,StopEllipse):
            out_data = self._calculateDataStopEllipse(beamline_component, in_data)
        elif isinstance(beamline_component, StopRectangle):
            out_data = self._calculateDataStopRectangle(beamline_component, in_data)
        elif isinstance(beamline_component, StopSquare):
            out_data = self._calculateDataStopSquare(beamline_component, in_data)

        # Screen
        if isinstance(optical_element, OpticalElementScreen):
            out_data = self._calculateDataScreen(optical_element, in_data)

        # Catch unhandled component.
        if out_data is None:
            raise Exception("Beamline component %s not implemented" % str(beamline_component))
        # TODO: FIX!!!
        if beamline_component is not None:
            del beamline_component._optical_element

        return out_data

    # Aperture
    def _calculateDataApertureCircle(self, beamline_component, in_data):
        """
        Calculates output data from input data for a aperture.
        """
        raise Exception("Needs reimplementation")

    def _calculateDataApertureEllipse(self, beamline_component, in_data):
        """
        Calculates output data from input data for a aperture.
        """
        raise Exception("Needs reimplementation")

    def _calculateDataApertureRectangle(self, beamline_component, in_data):
        """
        Calculates output data from input data for a aperture.
        """
        raise Exception("Needs reimplementation")

    def _calculateDataApertureSquare(self, beamline_component, in_data):
        """
        Calculates output data from input data for a aperture.
        """
        raise Exception("Needs reimplementation")

    # Driftspace
    def _calculateDataDriftSpace(self, beamline_component, in_data):
        """
        Calculates output data from input data for a drift space.
        """
        raise Exception("Needs reimplementation")

    # Lenses
    def _calculateDataLensIdeal(self, beamline_component, in_data):
        """
        Calculates output data from input data for an ideal lens.
        """
        raise Exception("Needs reimplementation")


    def _calculateDataElectronBeam(self, beamline_component, in_data):
        """
        Calculates output data from input data for an electron beam.
        """
        raise Exception("Needs reimplementation")

    # Sources
    def _calculateDataSourceGaussian(self, beamline_component, in_data):
        """
        Calculates output data from input data for a Gaussian source.
        """
        raise Exception("Needs reimplementation")

    def _calculateDataSourcePoint(self, beamline_component, in_data):
        """
        Calculates output data from input data for a point source.
        """
        raise Exception("Needs reimplementation")

    def _calculateDataUndulator(self, beamline_component, in_data):
        """
        Calculates output data from input data for an undulator.
        """
        raise Exception("Needs reimplementation")

    def _calculateDataWiggler(self, beamline_component, in_data):
        """
        Calculates output data from input data for a wiggler.
        """
        raise Exception("Needs reimplementation")

    # Screen
    def _calculateDataScreen(self, beamline_component, in_data):
        """
        Calculates output data from input data for a screen.
        """
        raise Exception("Needs reimplementation")   

    # Stop
    def _calculateDataStopCircle(self, beamline_component, in_data):
        """
        Calculates output data from input data for a aperture.
        """
        raise Exception("Needs reimplementation")

    def _calculateDataStopEllipse(self, beamline_component, in_data):
        """
        Calculates output data from input data for a aperture.
        """
        raise Exception("Needs reimplementation")

    def _calculateDataStopRectangle(self, beamline_component, in_data):
        """
        Calculates output data from input data for a aperture.
        """
        raise Exception("Needs reimplementation")

    def _calculateDataStopSquare(self, beamline_component, in_data):
        """
        Calculates output data from input data for a aperture.
        """
        raise Exception("Needs reimplementation")

    def driverSettings(self, beamline_component):
        """
        Returns the driver settings for the given beamline component.
        """
        # For the moment like this. Rethink if a more strict "splitting", i.e. the type like calculateData, is necessary.
        raise Exception("Needs reimplementation")   
    
    def calculateIntensity3D(self, in_data):
        """
        Calculates 3D intensity distribution.
        """
        raise Exception("Needs reimplementation")                

    def calculateIntensityHorizontalCut(self, in_data, horizontal_coordinate):
        """
        Calculates a horizontal intensity cut.
        """
        raise Exception("Needs reimplementation")

    def calculateIntensityVerticalCut(self, in_data, vertical_coordinate):
        """
        Calculates a vertical intensity cut.
        """
        raise Exception("Needs reimplementation")


    def calculatePhase3D(self, in_data):
        """
        Calculates 3D phase distribution.
        """
        raise Exception("Needs reimplementation")