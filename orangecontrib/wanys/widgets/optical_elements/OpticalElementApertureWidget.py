"""
<name>Optical aperture</name>
<description>An aperture</description>
<icon>icons/aperture.svg</icon>
<priority>10</priority>
"""
import sys
from PyQt4.Qt import *

from orangewidget.settings import Setting
from orangewidget import gui
from oasys.widgets import widget

from orangecontrib.wanys.BeamlineComponents.Aperture.ApertureCircle import ApertureCircle
from orangecontrib.wanys.BeamlineComponents.Aperture.ApertureRectangle import ApertureRectangle

from orangecontrib.wanys.util.Enum import Enum
from orangecontrib.wanys.util.OpticalElement import OpticalElement
from orangecontrib.wanys.util.OpticalBeam import OpticalBeam

from orangecontrib.wanys.widgets.drivers.DriverSettingsWidget import DriverSettingsWidget

class Circle(Enum):
    def __init__(self):
        Enum.__init__(self, "Circle")

class Rectangle(Enum):
    def __init__(self):
        Enum.__init__(self, "Rectangle")


class OpticalElementApertureWidget(widget.OWWidget):
    name = "Optical aperture"
    description = "Optical aperture"
    icon = "icons/aperture.svg"
    
    inputs  = [("Optical beam", OpticalBeam, "onOpticalBeam", widget.Multiple)]
    outputs = [("Optical beam", OpticalBeam)]

    want_main_area = False

    value_cbb_aperture_type = Setting(0)

    value_le_diameter = Setting(1.0)
    value_le_width = Setting(1.0)
    value_le_height = Setting(1.0)
    
    value_le_driver_settings = Setting("")
         
    def __init__(self, parent=None, signalManager=None):
        widget.OWWidget.__init__(self, parent, signalManager)

        self.__optical_aperture = OpticalElement("aperture")
       

        geometries = ["Circle", "Rectangle"]
        self.geometries_mapping = {0 : Circle(),
                                   1 : Rectangle()}
            
        self.cbb_geometry_type = gui.comboBox(self.controlArea,
                                              self,
                                              "value_cbb_aperture_type",
                                              box=None,
                                              label = "Aperture type",
                                              items = geometries,
                                              callback=self.cbb_geometry_change)
       
        self.le_diameter = gui.lineEdit(self.controlArea,
                                        self,
                                        "value_le_diameter",
                                        label="Diameter [m]",
                                        validator=QDoubleValidator(bottom=0.0))
        
        self.le_width = gui.lineEdit(self.controlArea,
                                     self,
                                     "value_le_width",
                                     label="Width [m]",
                                     validator=QDoubleValidator(bottom=0.0))

        self.le_height = gui.lineEdit(self.controlArea,
                                      self,
                                      "value_le_height",
                                      label="Height [m]",
                                      validator=QDoubleValidator(bottom=0.0))

        self.__driver_settings_widget = DriverSettingsWidget(self.__optical_aperture,
                                                             self,
                                                             "value_le_driver_settings")

        self.__optical_aperture.setOnSynchronize(self.synchronizeToOpticalElement)      
        self.__optical_aperture.setOnCalculationStart(self.calculationStart)      
        self.__optical_aperture.setOnCalculationFinished(self.calculationFinished)
        
        self._updateEnableStates()      

    def calculationStart(self):
        self.progressBarInit()
        self.progressBarSet(0)
        QApplication.processEvents()

    def calculationFinished(self):
        self.progressBarSet(100)
        QApplication.processEvents()

    def _selectedApertureType(self):
        aperture_type_index = int(self.value_cbb_aperture_type)
        aperture = self.geometries_mapping[aperture_type_index]
        return aperture

    def synchronizeToOpticalElement(self):
        aperture = self._selectedApertureType()

        if aperture == Circle():
            diameter = float(self.value_le_diameter)
            beamline_component = ApertureCircle(diameter=diameter)
        elif aperture == Rectangle():
            width = float(self.value_le_width)
            height = float(self.value_le_height)

            beamline_component = ApertureRectangle(length_vertical=height, length_horizontal=width)

        self.__optical_aperture.setBeamlineComponent(beamline_component=beamline_component)
        
    def onOpticalBeam(self, optical_beam, sender):   
        print("OPTAPT SENDER", sender)
        optical_beam.sender().addOutput(self.__optical_aperture)
        
        sender = OpticalBeam(self.__optical_aperture)
        self.send("Optical beam", sender)
        for i in range(1000000):
            QApplication.processEvents()

    
    def _updateEnableStates(self):
        aperture = self._selectedApertureType()

        if aperture == Circle():
            self.le_diameter.setEnabled(True)            
            self.le_width.setEnabled(False)
            self.le_height.setEnabled(False)
        elif aperture == Rectangle():
            self.le_diameter.setEnabled(False)            
            self.le_width.setEnabled(True)
            self.le_height.setEnabled(True)
        
    
    def cbb_geometry_change(self):
        self._updateEnableStates()
    
if __name__=="__main__":
    appl = QApplication(sys.argv)
    ow = OpticalElementApertureWidget()
    ow.show()
    appl.exec_()
