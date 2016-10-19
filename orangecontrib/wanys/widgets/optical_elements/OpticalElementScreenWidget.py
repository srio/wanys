"""
<name>Optical screen</name>
<description>Display an optical beam</description>
<icon>icons/screen.svg</icon>
<priority>10</priority>
"""

from PyQt4.Qt import *

from orangewidget import gui
from oasys.widgets import widget

from matplotlib.pyplot import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt
from array import array
import numpy as np

from orangecontrib.wanys.util.OpticalElementScreen import OpticalElementScreen
from orangecontrib.wanys.util.OpticalBeam import OpticalBeam
from orangecontrib.wanys.drivers.srw.LSFApproximation import plotSurface
from orangecontrib.wanys.drivers.ActiveDriver import ActiveDriver

class PlotSetModel(QAbstractTableModel):
    def __init__(self, plots_list):
        super(PlotSetModel, self).__init__()
        self._plots_list = plots_list
        
    def _plotsList(self):
        return self._plots_list
        
    def rowCount(self, index=QModelIndex()):
        return len(self._plotsList())

    def columnCount(self, index=QModelIndex()):
        return 1
    
    def headerData(self, column_offset, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation==Qt.Horizontal:
                if column_offset==0:
                    return "Name"
                
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() \
           or \
           not(0<=index.row()<=len(self._plotsList())):
            print(index.row())
            return QVariant()
        
        if role != Qt.DisplayRole:
            return None
        
        if index.column()==0:
            #item = self._plotsList()[int(index.row())]
            #item = item.title()
            item = str(index.row())
        else:
            return None
        
        return item    
    
    def plotByIndex(self, index):
        return self._plotsList()[index]

class OpticalElementScreenWidget(widget.OWWidget):
    name = "Optical screen"
    description = "Optical screen"
    icon = "icons/screen.svg"

    want_main_area = False
    want_control_area = False

    inputs  = [("Optical beam", OpticalBeam, "onOpticalBeam", widget.Multiple)]
      
    def __init__(self, parent=None, signalManager=None):
        widget.OWWidget.__init__(self, parent, signalManager)

        self.__optical_screen = OpticalElementScreen("screen")

        self.combobox = QComboBox()
        self.connect(self.combobox, 
                     SIGNAL("currentIndexChanged(int)"), 
                     self.plots_combobox_index_changed)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.btn_vertical_cut = gui.button(self,
                                           self,
                                           "Vertical cut",
                                           self.onVerticalCut)

        self.btn_horizontal_cut = gui.button(self,
                                             self,
                                             "Horizontal cut",
                                              self.onHorizontalCut)


        self.btn_plot_surface = gui.button(self,
                                           self,
                                           "Surface plot",
                                           self.onPlotSurface)


        self.layout().addWidget(self.combobox)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)
        self.layout().addWidget(self.btn_vertical_cut)
        self.layout().addWidget(self.btn_horizontal_cut)
        self.layout().addWidget(self.btn_plot_surface)

        self.__optical_screen.setOnCalculationFinished(self.calculationFinished)      

    def calculationFinished(self):
        self.progressBarInit()
        self.progressBarSet(0)
        QApplication.processEvents()
        self.display()
        self.progressBarSet(100)
        QApplication.processEvents()
        self.show()
        
    def onOpticalBeam(self, optical_beam, sender):
        optical_beam.sender().addOutput(self.__optical_screen)

    def plots_combobox_index_changed(self, index):
        plot = self.combobox.model().plotByIndex(index)

        self.my_plot(plot[0], 
                     plot[1],
                     plot[2])

        self._plot = plot

    def display(self):

        driver = ActiveDriver().driver()

        print(self.__optical_screen.calculateIntensity3D(driver).keys())
        
        res = []
        for intensity in list(self.__optical_screen.calculateIntensity3D(driver).values()):
            res.append([intensity[0],
                        intensity[1],
                        intensity[2]])
        self.model_plots = PlotSetModel(res)
        self.combobox.setModel(self.model_plots)
        
    
    def my_plot(self, ar2d, x_range, y_range):
        
        fig = self.figure
        ax = fig.add_subplot(111)
        ax.hold(False)
    
        totLen = int(x_range[2]*y_range[2])
        lenAr2d = len(ar2d)
        if lenAr2d > totLen: 
            ar2d = np.array(ar2d[0:totLen])
        elif lenAr2d < totLen:
            auxAr = array('f', [0]*lenAr2d)
            for i in range(lenAr2d): 
                auxAr[i] = ar2d[i]
            ar2d = np.array(auxAr)

        if isinstance(ar2d,(list,array)): 
            ar2d = np.array(ar2d)
    
            ar2d = ar2d.reshape(y_range[2],x_range[2])

        x = np.linspace(x_range[0],x_range[1],x_range[2])
        y = np.linspace(y_range[0],y_range[1],y_range[2])
    
        ax.pcolormesh(x,y,ar2d,cmap=cm.Greys_r) #OC150814
            
        ax.set_xlim(x[0],x[-1])
        ax.set_ylim(y[0],y[-1])
        ax.set_xlabel("X coordinate")
        ax.set_ylabel("Y coordinate")
    
        #if(len(labels) > 2):
        ax.set_title("Intensity")
        #show()
        self.canvas.draw()

    def onVerticalCut(self):
        driver = ActiveDriver().driver()
        for intensity in list(self.__optical_screen.calculateIntensityVerticalCut(driver,vertical_coordinate=None).values()):
            print("MAX INTENSITY OVER e: ",np.array(intensity[1]).max() * 0.5)
            plt.plot(intensity[0],intensity[1], intensity[0], [np.array(intensity[1]).max() * 0.5] * len(intensity[0]))
            plt.show()


    def onHorizontalCut(self):
        driver = ActiveDriver().driver()
        res = []
        for intensity in list(self.__optical_screen.calculateIntensityHorizontalCut(driver, horizontal_coordinate=None).values()):
            print("MAX INTENSITY OVER e: ",np.array(intensity[1]).max() * 0.5)
            plt.plot(intensity[0],intensity[1], intensity[0], [np.array(intensity[1]).max() * 0.5] * len(intensity[0]))
            plt.show()

    def onPlotSurface(self):
        x_range = self._plot[1]
        y_range = self._plot[2]
        ar2d = self._plot[0]

        totLen = int(x_range[2]*y_range[2])
        lenAr2d = len(ar2d)
        if lenAr2d > totLen:
            ar2d = np.array(ar2d[0:totLen])
        elif lenAr2d < totLen:
            auxAr = array('f', [0]*lenAr2d)
            for i in range(lenAr2d):
                auxAr[i] = ar2d[i]
            ar2d = np.array(auxAr)

        if isinstance(ar2d,(list,array)):
            ar2d = np.array(ar2d)

            ar2d = ar2d.reshape(y_range[2],x_range[2])

        x = np.linspace(x_range[0],x_range[1],x_range[2])
        y = np.linspace(y_range[0],y_range[1],y_range[2])


        plotSurface(x,y,ar2d)

if __name__=="__main__":
    appl = QApplication(sys.argv)
    ow = OpticalElementScreenWidget()
    ow.show()
    appl.exec_()
