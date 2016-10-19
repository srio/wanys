"""
<name>Gaussian source</name>
<description>A Gaussian source</description>
<icon>icons/gaussian.svg</icon>
<priority>100</priority>
"""
import sys
from PyQt4.Qt import *


from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import widget

from orangecontrib.wanys.util.OpticalElement import OpticalElement
from orangecontrib.wanys.util.OpticalBeam import OpticalBeam
from orangecontrib.wanys.util.Polarization import Polarization

from orangecontrib.wanys.widgets.drivers.DriverSettingsWidget import DriverSettingsWidget
from orangecontrib.wanys.drivers.ActiveDriver import ActiveDriver

from BeamlineComponents.Source.SourceGaussian import SourceGaussian

class OpticalElementSourceGaussianWidget(widget.OWWidget):
    name = "Gaussian source"
    description = "Gaussian source"
    icon = "icons/gaussian.svg"
    
    outputs = [("Optical beam", OpticalBeam)]

    want_main_area = False

    value_le_x = Setting(0)
    value_le_y = Setting(0)
    value_le_z = Setting(0)

    value_le_sigma_x = Setting(23e-06/2.35)
    value_le_sigma_y = Setting(23e-06/2.35)

    value_le_sigma_x_prime = Setting(0.0)
    value_le_sigma_y_prime = Setting(0.0)

    value_le_sigma_t = Setting(10e-15)


    value_le_xp = Setting(0)
    value_le_yp = Setting(0)
    
    value_le_average_photon_energy = Setting(8000.0)
    value_le_pulse_energy = Setting(0.001)
    
    value_le_repetition_rate = Setting(1)
    value_cb_polarization = Setting(1)
    value_le_driver_settings = Setting("")
         
    def __init__(self, parent=None, signalManager=None):
        widget.OWWidget.__init__(self, parent, signalManager)

        self.__optical_source_gaussian = OpticalElement("source gaussian")
       
        self.le_x = gui.lineEdit(self.controlArea,
                                 self,
                                 "value_le_x",
                                 label="X [m]",
                                 validator=QDoubleValidator(bottom=0.0))
        
        self.le_y = gui.lineEdit(self.controlArea,
                                 self,
                                 "value_le_y",
                                 label="Y [m]",
                                 validator=QDoubleValidator(bottom=0.0))

        self.le_z = gui.lineEdit(self.controlArea,
                                 self,
                                 "value_le_z",
                                 label="Z [m]",
                                 validator=QDoubleValidator(bottom=0.0))

        self.le_sigma_x = gui.lineEdit(self.controlArea,
                                       self,
                                       "value_le_sigma_x",
                                       label="sigma X [m]",
                                       validator=QDoubleValidator(bottom=0.0))
        
        self.le_sigma_y = gui.lineEdit(self.controlArea,
                                       self,
                                       "value_le_sigma_y",
                                       label="sigma Y [m]",
                                       validator=QDoubleValidator(bottom=0.0))

        self.le_sigma_x_prime = gui.lineEdit(self.controlArea,
                                             self,
                                             "value_le_sigma_x_prime",
                                             label="sigma X prime [m]",
                                             validator=QDoubleValidator(bottom=0.0))

        self.le_sigma_y_prime = gui.lineEdit(self.controlArea,
                                             self,
                                             "value_le_sigma_y_prime",
                                             label="sigma Y prime [m]",
                                             validator=QDoubleValidator(bottom=0.0))

        self.le_sigma_t = gui.lineEdit(self.controlArea,
                                       self,
                                       "value_le_sigma_t",
                                       label="sigma t [m]",
                                       validator=QDoubleValidator(bottom=0.0))


        self.le_xp = gui.lineEdit(self.controlArea,
                                  self,
                                  "value_le_xp",
                                  label="Xp [m]",
                                  validator=QDoubleValidator(bottom=0.0))
        
        self.le_yp = gui.lineEdit(self.controlArea,
                                  self,
                                  "value_le_yp",
                                  label="Yp [m]",
                                  validator=QDoubleValidator(bottom=0.0))

        self.le_average_photon_energy = gui.lineEdit(self.controlArea,
                                                     self,
                                                     "value_le_average_photon_energy",
                                                     label="Average photon energy [eV]",
                                                     validator=QDoubleValidator(bottom=0.0))
        
        self.le_pulse_energy = gui.lineEdit(self.controlArea,
                                            self,
                                            "value_le_pulse_energy",
                                            label="Pulse energy [J]",
                                            validator=QDoubleValidator(bottom=0.0))

        self.le_repetition_rate = gui.lineEdit(self.controlArea,
                                               self,
                                               "value_le_repetition_rate",
                                               label="Repetition rate",
                                               validator=QIntValidator(bottom=0))
        
        self.polarizations=Polarization.all()
        self.cb_polarization = gui.comboBox(self.controlArea,
                                            self,
                                            "value_cb_polarization",
                                            label="Polarization",
                                            items=[p.description() for p in self.polarizations])

        # TODO: refactor beamline component passing.
        self.__driver_settings_widget = DriverSettingsWidget(self.__optical_source_gaussian, 
                                                             self,
                                                             "value_le_driver_settings",
                                                             SourceGaussian(0.0,0.0,0.0,0.0,0.0))

        self.btn_display = gui.button(self,
                                      self,
                                      "Fire",
                                      self.onFire)  
        
        
        self.__optical_source_gaussian.setOnSynchronize(self.synchronizeToOpticalElement)      

        self.__optical_source_gaussian.setOnCalculationStart(self.calculationStart)      
        self.__optical_source_gaussian.setOnCalculationFinished(self.calculationFinished)      


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
        source = self.__optical_source_gaussian
        
        #source.setX(float(self.value_le_x))
        #source.setY(float(self.value_le_y))
        #source.setZ(float(self.value_le_z))
        
        sigma_x = float(self.value_le_sigma_x)
        sigma_y = float(self.value_le_sigma_y)

        sigma_x_prime = float(self.value_le_sigma_x_prime)
        sigma_y_prime = float(self.value_le_sigma_y_prime)


        #source.setSigmaT(float(self.value_le_sigma_t))

        #source.setXp(float(self.value_le_xp))
        #source.setYp(float(self.value_le_yp))
        
        energy = float(self.value_le_average_photon_energy)
        #source.setPulseEnergy(float(self.value_le_pulse_energy))
        #source.setRepititionRate(float(self.value_le_repetition_rate))
        #source.setPolarization(self.polarizations[int(self.value_cb_polarization)])

        beamline_component = SourceGaussian(sigma_x=sigma_x,
                                            sigma_y=sigma_y,
                                            sigma_x_prime=sigma_x_prime,
                                            sigma_y_prime=sigma_y_prime,
                                            energy=energy)

        source.setBeamlineComponent(beamline_component)

    def onFire(self):

        beam = OpticalBeam(self.__optical_source_gaussian)
        
        self.send("Optical beam", beam)
        for i in range(1000000):
            QApplication.processEvents()

        driver = ActiveDriver().driver()
        self.__optical_source_gaussian.startTravers(driver)


if __name__=="__main__":
    appl = QApplication(sys.argv)
    ow = OpticalElementSourceGaussianWidget()
    ow.show()
    appl.exec_()
