"""
<name>Optical lens</name>
<description>An ideal lens</description>
<icon>icons/lens.svg</icon>
<priority>10</priority>
"""
import sys
from PyQt4.Qt import *

from orangewidget.settings import Setting
from orangewidget import gui
from oasys.widgets import widget

from orangecontrib.wanys.util.OpticalElement import OpticalElement
from orangecontrib.wanys.util.OpticalBeam import OpticalBeam
from orangecontrib.wanys.widgets.drivers.DriverSettingsWidget import DriverSettingsWidget

from BeamlineComponents.Lens.LensIdeal import LensIdeal

class OpticalElementLensWidget(widget.OWWidget):
    name = "Optical lens"
    description = "Optical lens"
    icon = "icons/lens.svg"
    
    inputs  = [("Optical beam", OpticalBeam, "onOpticalBeam", widget.Multiple)]
    outputs = [("Optical beam", OpticalBeam)]    

    value_le_focal_x = Setting(1.0)
    value_le_focal_y = Setting(1.0)

    value_le_driver_settings = Setting("")

    want_main_area = False

    def __init__(self, parent=None, signalManager=None):
        widget.OWWidget.__init__(self, parent, signalManager)

        self.__optical_lens = OpticalElement("lens")
       
        self.le_focal_x = gui.lineEdit(self.controlArea,
                                       self,
                                       "value_le_focal_x",
                                       label="Focal length x [m]",
                                       validator=QDoubleValidator(bottom=0.0))
        
        self.le_focal_y = gui.lineEdit(self.controlArea,
                                       self,
                                       "value_le_focal_y",
                                       label="Focal length y [m]",
                                       validator=QDoubleValidator(bottom=0.0))

        self.__driver_settings_widget = DriverSettingsWidget(self.__optical_lens, 
                                                             self,
                                                             "value_le_driver_settings")
        self.__optical_lens.setOnSynchronize(self.synchronizeToOpticalElement)      
        self.__optical_lens.setOnCalculationStart(self.calculationStart)      
        self.__optical_lens.setOnCalculationFinished(self.calculationFinished)      

    def calculationStart(self):
        self.progressBarInit()
        self.progressBarSet(0)
        QApplication.processEvents()

    def calculationFinished(self):
        self.progressBarSet(100)
        QApplication.processEvents()
        
    def synchronizeToOpticalElement(self):
        focal_x = float(self.value_le_focal_x)
        focal_y = float(self.value_le_focal_y)

        beamline_component = LensIdeal(focal_x=focal_x,
                                       focal_y=focal_y)
        self.__optical_lens.setBeamlineComponent(beamline_component=beamline_component)

    def onOpticalBeam(self, optical_beam, sender):
        optical_beam.sender().addOutput(self.__optical_lens)
                
        sender = OpticalBeam(self.__optical_lens)
        self.send("Optical beam", sender)

if __name__=="__main__":
    appl = QApplication(sys.argv)
    ow = OpticalElementLensWidget()
    ow.show()
    appl.exec_()
