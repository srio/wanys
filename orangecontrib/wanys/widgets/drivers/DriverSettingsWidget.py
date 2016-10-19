"""
Widget for driver settings.
"""
import sys
from PyQt4 import *
from PyQt4.QtGui import *
from PyQt4.Qt import *

# from Orange.widgets import widget, settings, gui
# import Orange.data

from orangewidget import gui
from oasys.widgets import widget

from orangecontrib.wanys.util.OpticalElement import OpticalElement
from orangecontrib.wanys.drivers.DriverSettings import DriverSettings
from orangecontrib.wanys.drivers.ActiveDriver import ActiveDriver

class DriverSettingsDialog(QDialog):
    def __init__(self, driver_settings=None, parent=None, beamline_component=None):
        QDialog.__init__(self, parent)
        
        driver = ActiveDriver().driver()


        if driver_settings is None:
            self.__settings = driver.driverSettings(beamline_component)
        else:
            if driver_settings.isDriver(driver):
                self.__settings = driver_settings
            else:
                self.__settings = driver.driverSettings(beamline_component)
        
        self.__labels = []
        self.__le = []
        self.__cb = []
        
        self.__vbox = QVBoxLayout()
        
        self._constructFromSettings(self.__settings)
        self.__btn_close = QPushButton("Close")
        self.connect(self.__btn_close,SIGNAL('clicked()'), self.on_btn_close)
        self.__vbox.addWidget(self.__btn_close)
        
        self.setLayout(self.__vbox)
        
    def driverSettings(self):
        return self.__settings

    def _createLineEdit(self, name, description, value):
        le = QLineEdit()
        le.setObjectName(name)
        le.setText(str(value))
        le.setToolTip(description)
        label = QLabel(name)
        label.setBuddy(le)
        
        self.__labels.append(label)

        self.__vbox.addWidget(label)        
        self.__vbox.addWidget(le)
        self.__le.append(le)
            
    def _createComboboxTrueFalse(self, name, description, value):
        cb = QComboBox(self)
        cb.addItem("True", True)
        cb.addItem("False", False)

        cb.setObjectName(name)
        cb.setToolTip(description)
        label = QLabel(name)
        label.setBuddy(cb)
        
        index = cb.findData(value)
        cb.setCurrentIndex(index)
        
        self.__labels.append(label)

        self.__vbox.addWidget(label)        
        self.__vbox.addWidget(cb)
        self.__cb.append(cb)

        
    def _constructAttributeString(self, name, description, value):
        self._createLineEdit(name, description, value)

    def _constructAttributeBoolean(self, name, description, value):
        self._createComboboxTrueFalse(name, description, value)

    def _constructAttributeInteger(self, name, description, value):
        self._createLineEdit(name, description, value)

    def _constructAttributeFloat(self, name, description, value):
        self._createLineEdit(name, description, value)
        
    def _constructFromSettings(self, settings):
        for name in settings.names():
            attribute_type = settings.typeByName(name)
            description    = settings.descriptionByName(name)
            value          = settings.valueByName(name)
            
            if attribute_type is str:
                self._constructAttributeString(name, description, value)
            elif attribute_type is bool:
                self._constructAttributeBoolean(name, description, value)
            elif attribute_type is int:
                self._constructAttributeInteger(name, description, value)
            elif attribute_type is float:
                self._constructAttributeFloat(name, description, value)
            else:
                raise Exception("Attribute type %s not handled." % attribute_type)

    def updateDriverSettings(self):
        for le_or_cb in self.__le + self.__cb:
            name = le_or_cb.objectName()
            a_type = self.__settings.typeByName(name)
            
            if a_type is str:
                value = str(le_or_cb.text())
            elif a_type is int:
                value = int(le_or_cb.text())
            elif a_type is float:
                value = float(le_or_cb.text())
            elif a_type is bool:
                value = bool(le_or_cb.itemData(le_or_cb.currentIndex()))
            else:
                raise Exception("Unhandled type")
            
            self.__settings.setValueByName(name, value)
            

    def on_btn_close(self):
        self.close()

    def closeEvent(self, event):
        self.updateDriverSettings()

class DriverSettingsWidget(widget.OWWidget):

    def __init__(self, optical_element, orange_widget, value_le, beamline_component=None):
        QWidget.__init__(self, None)

        self.le_x = gui.lineEdit(orange_widget,
                                 orange_widget,
                                 value_le)        
        self.le_x.setVisible(False)

        
        self.__optical_element = optical_element
        self.__hbox = QHBoxLayout()
        self.__btn_driver_settings = QPushButton("Driver settings")
        self._beamline_component = beamline_component
        
        self.__orange_widget = orange_widget
        
        driver_settings_as_string = self.le_x.text()
        if driver_settings_as_string == "":
            self.__driver_settings = None
        else:
            try:
                self.__driver_settings = DriverSettings.loadFromString(eval(driver_settings_as_string))
                self.__optical_element.setDriverSettings(self.driverSettings())
            except:
                self.__driver_settings = None

        self.__hbox.addWidget(self.__btn_driver_settings)
        self.setLayout(self.__hbox)
        
        self.connect(self.__btn_driver_settings,SIGNAL("clicked()"),self.btn_driver_settings_clicked)

        self.__orange_widget.layout().addWidget(self)


    def btn_driver_settings_clicked(self):
        
        dialog = DriverSettingsDialog(self.driverSettings(), beamline_component=self._beamline_component)
        dialog.exec_()
        self.__driver_settings = dialog.driverSettings()
        
        self.__optical_element.setDriverSettings(self.driverSettings())
        self.le_x.setText(self.asString())
        
    def driverSettings(self):
        return self.__driver_settings

    def asString(self):
        return str(self.driverSettings().saveAsString())


if __name__=="__main__":
    appl = QApplication(sys.argv)
    parent = widget.OWWidget()
    ow = DriverSettingsWidget(OpticalElement("type"),parent,0)
    parent.show()
    appl.exec_()
