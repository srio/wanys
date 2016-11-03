"""
<name>Undulator</name>
<description>An undulator</description>
<icon>icons/gaussian.svg</icon>
<priority>2</priority>
"""
import sys
from PyQt4.Qt import *

from orangewidget.settings import Setting
from orangewidget import gui
from oasys.widgets import widget

from orangecontrib.wanys.util.OpticalElement import OpticalElement
from orangecontrib.wanys.util.OpticalBeam import OpticalBeam
from orangecontrib.wanys.widgets.drivers.DriverSettingsWidget import DriverSettingsWidget

from orangecontrib.wanys.BeamlineComponents.Source.Undulator import Undulator

class UndulatorWidget(widget.OWWidget):
    name = "Undulator"
    description = "Undulator"
    icon = "icons/gaussian.svg"

    want_main_area = False

    inputs  = [("Optical beam", OpticalBeam, "onOpticalBeam", widget.Multiple)]
    outputs = [("Optical beam", OpticalBeam)]

    value_le_K_vertical = Setting(1.87)
    value_le_K_horizontal = Setting(0)
    value_le_period_length = Setting(0.035)
    value_le_period_number = Setting(14)

    value_le_driver_settings = Setting("")

    def __init__(self, parent=None, signalManager=None):
        widget.OWWidget.__init__(self, parent, signalManager)

        self.__optical_undulator = OpticalElement("undulator")


        self.le_K_vertical = gui.lineEdit(self.controlArea,
                                          self,
                                          "value_le_K_vertical",
                                          label="Vertical K",
                                          validator=QDoubleValidator(bottom=0.0))

        self.le_K_horizontal = gui.lineEdit(self.controlArea,
                                            self,
                                            "value_le_K_horizontal",
                                            label="Horizontal K",
                                            validator=QDoubleValidator(bottom=0.0))

        self.le_period_length = gui.lineEdit(self.controlArea,
                                             self,
                                             "value_le_period_length",
                                             label="period length [m]",
                                             validator=QDoubleValidator(bottom=0.0))

        self.le_period_number = gui.lineEdit(self.controlArea,
                                             self,
                                             "value_le_period_number",
                                             label="number periods",
                                             validator=QDoubleValidator(bottom=0.0))


        self.__driver_settings_widget = DriverSettingsWidget(self.__optical_undulator,
                                                             self,
                                                             "value_le_driver_settings",
                                                             Undulator(1.8,1.8,0.35,100))

        self.__optical_undulator.setOnSynchronize(self.synchronizeToOpticalElement)

    def synchronizeToOpticalElement(self):
        source = self.__optical_undulator

        K_vertical = float(self.value_le_K_vertical)
        K_horizontal = float(self.value_le_K_horizontal)
        period_length = float(self.value_le_period_length)
        period_number =float(self.value_le_period_number)

        beamline_component = Undulator(K_vertical=K_vertical,
                                       K_horizontal=K_horizontal,
                                       period_length=period_length,
                                       periods_number=period_number)
        self.__optical_undulator.setBeamlineComponent(beamline_component=beamline_component)

    def onOpticalBeam(self, optical_beam, sender):
        optical_beam.sender().addOutput(self.__optical_undulator)

        sender = OpticalBeam(self.__optical_undulator)
        self.send("Optical beam", sender)


if __name__=="__main__":
    appl = QApplication(sys.argv)
    ow = UndulatorWidget()
    ow.show()
    appl.exec_()
