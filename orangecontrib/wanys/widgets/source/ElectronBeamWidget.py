"""
<name>Electron beam</name>
<description>An electron beam</description>
<icon>icons/gaussian.svg</icon>
<priority>1</priority>
"""
import sys
from PyQt4.Qt import *


from orangewidget.settings import Setting
from orangewidget import gui
from oasys.widgets import widget


from orangecontrib.wanys.util.OpticalElement import OpticalElement
from orangecontrib.wanys.util.OpticalBeam import OpticalBeam
from orangecontrib.wanys.widgets.drivers.DriverSettingsWidget import DriverSettingsWidget
from orangecontrib.wanys.drivers.ActiveDriver import ActiveDriver

from BeamlineComponents.Beam.ElectronBeam import ElectronBeam

class ElectronBeamWidget(widget.OWWidget):
    name = "Electron beam"
    description = "Electron beam"
    icon = "icons/gaussian.svg"

    outputs = [("Optical beam", OpticalBeam)]

    want_main_area = False

    value_le_energy = Setting(6.0)
    value_le_energy_spread = Setting(0)
    value_le_average_current = Setting(0.2)
    value_le_electrons = Setting(1)

    value_le_driver_settings = Setting("")

    def __init__(self, parent=None, signalManager=None):
        widget.OWWidget.__init__(self, parent, signalManager)

        self.__optical_electron_beam = OpticalElement("electron beam")

        self.le_energy = gui.lineEdit(self.controlArea,
                                      self,
                                      "value_le_energy",
                                      label="Energy [GeV]",
                                      validator=QDoubleValidator(bottom=0.0))

        self.le_energy_spread = gui.lineEdit(self.controlArea,
                                             self,
                                             "value_le_energy_spread",
                                             label="Energy spread",
                                             validator=QDoubleValidator(bottom=0.0))

        self.le_average_current = gui.lineEdit(self.controlArea,
                                               self,
                                               "value_le_average_current",
                                               label="Average current [A]",
                                               validator=QDoubleValidator(bottom=0.0))

        self.le_electrons = gui.lineEdit(self.controlArea,
                                         self,
                                         "value_le_electrons",
                                         label="Electrons in bunch",
                                         validator=QDoubleValidator(bottom=0.0))



        self.__driver_settings_widget = DriverSettingsWidget(self.__optical_electron_beam,
                                                             self,
                                                             "value_le_driver_settings")

        self.btn_display = gui.button(self,
                                      self,
                                      "Fire",
                                      self.onFire)


        self.__optical_electron_beam.setOnSynchronize(self.synchronizeToOpticalElement)

        self.__optical_electron_beam.setOnCalculationStart(self.calculationStart)
        self.__optical_electron_beam.setOnCalculationFinished(self.calculationFinished)


    def calculationStart(self):
        return
        self.progressBarInit()
        self.progressBarSet(0)
        QApplication.processEvents()

    def calculationFinished(self):
        #self.progressBarInit()
        #self.progressBarSet(100)
        return

    def synchronizeToOpticalElement(self):
        source = self.__optical_electron_beam

        average_current = float(self.value_le_average_current)
        energy_spread = float(self.value_le_energy_spread)
        energy_in_GeV = float(self.value_le_energy)
        electrons = float(self.value_le_electrons)

        beamline_component = ElectronBeam(energy_in_GeV, energy_spread, average_current, electrons)
        source.setBeamlineComponent(beamline_component)


    def onFire(self):
        beam = OpticalBeam(self.__optical_electron_beam)

        self.send("Optical beam", beam)
        for i in range(10000):
            QApplication.processEvents()

        driver = ActiveDriver().driver()
        self.__optical_electron_beam.startTravers(driver)


if __name__=="__main__":
    appl = QApplication(sys.argv)
    ow = ElectronBeamWidget()
    ow.show()
    appl.exec_()
