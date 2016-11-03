"""
<name>Optical drift space</name>
<description>Drift space</description>
<icon>icons/drift_space.svg</icon>
<priority>10</priority>
"""
import sys
from PyQt4.Qt import *

from orangewidget.settings import Setting
from orangewidget import gui
from oasys.widgets import widget

from orangecontrib.wanys.util.OpticalElement import OpticalElement
from orangecontrib.wanys.util.OpticalBeam import OpticalBeam

from orangecontrib.wanys.BeamlineComponents.DriftSpace.DriftSpace import DriftSpace

from orangecontrib.wanys.widgets.drivers.DriverSettingsWidget import DriverSettingsWidget

class OpticalElementSpaceWidget(widget.OWWidget):
    name = "Drift space"
    description = "Drift space"
    icon = "icons/drift_space.svg"

    want_main_area = False

    inputs  = [("Optical beam", OpticalBeam, "onOpticalBeam",widget.Multiple)]
    outputs = [("Optical beam", OpticalBeam)]
    
    value_le_length = Setting(1.0)
    
    value_le_driver_settings = Setting("")
        
    def __init__(self, parent=None, signalManager=None):
        widget.OWWidget.__init__(self, parent, signalManager)

        self.__optical_space = OpticalElement("driftspace")
       
        self.le_length = gui.lineEdit(self.controlArea,
                                      self,
                                      "value_le_length",
                                      label="Length [m]",
                                      validator=QDoubleValidator(bottom=0.0))

        self.__driver_settings_widget = DriverSettingsWidget(self.__optical_space,
                                                             self,
                                                             "value_le_driver_settings")
        
        self.__optical_space.setOnSynchronize(self.synchronizeToOpticalElement)      
        self.__optical_space.setOnCalculationStart(self.calculationStart)      
        self.__optical_space.setOnCalculationFinished(self.calculationFinished)      

    def calculationStart(self):
        self.progressBarInit()
        self.progressBarSet(0)
        QApplication.processEvents()

    def calculationFinished(self):
        self.progressBarSet(100)
        QApplication.processEvents()

    def synchronizeToOpticalElement(self):
        length = float(self.value_le_length)
        beamline_component = DriftSpace(length)
        self.__optical_space.setBeamlineComponent(beamline_component=beamline_component)
                
    def onOpticalBeam(self, optical_beam, sender):
        optical_beam.sender().addOutput(self.__optical_space)
        
        sender = OpticalBeam(self.__optical_space)
        self.send("Optical beam", sender)


if __name__=="__main__":
    appl = QApplication(sys.argv)
    ow = OpticalElementSpaceWidget()
    ow.show()
    appl.exec_()
