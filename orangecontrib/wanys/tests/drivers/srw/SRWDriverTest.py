"""
Test for SRW driver.
"""
import unittest
from orangecontrib.srw.util.OpticalElementSourceGaussian import OpticalElementSourceGaussian
from orangecontrib.srw.util.OpticalElementAperture import OpticalElementAperture
from orangecontrib.srw.util.OpticalElementLens import OpticalElementLens
from orangecontrib.srw.util.OpticalElementScreen import OpticalElementScreen
from orangecontrib.srw.util.OpticalElementSpace import OpticalElementSpace
from orangecontrib.srw.util.OpticalElementAperture import Disc
from orangecontrib.srw.util.Polarization import LinearHorizontal

from orangecontrib.srw.drivers.srw.SRWDriver import SRWDriver

from matplotlib import *
from matplotlib.pyplot import *
import array


def my_plot(ar2d, x_range, y_range):
    import numpy as np
    
    fig = figure()
    typ = 111
    
    totLen = int(x_range[2]*y_range[2])
    lenAr2d = len(ar2d)
    if lenAr2d > totLen: 
        ar2d = np.array(ar2d[0:totLen])
    elif lenAr2d < totLen:
            auxAr = np.array('d', [0]*lenAr2d)
            for i in range(lenAr2d): auxAr[i] = ar2d[i]
            ar2d = np.array(auxAr)

    if isinstance(ar2d,(list,array.array)): 
        ar2d = np.array(ar2d)
    
    ar2d = ar2d.reshape(y_range[2],x_range[2])

    x = np.linspace(x_range[0],x_range[1],x_range[2])
    y = np.linspace(y_range[0],y_range[1],y_range[2])
    ax = fig.add_subplot(typ)

    ax.pcolormesh(x,y,ar2d,cmap=cm.Greys_r) #OC150814
        
    ax.set_xlim(x[0],x[-1])
    ax.set_ylim(y[0],y[-1])
    #ax.set_xlabel(labels[0])
    #ax.set_ylabel(labels[1])

    show()

class SRWDriverTest(unittest.TestCase):
    def testConstructor(self):
        driver = SRWDriver()
        
        self.assertIsInstance(driver, SRWDriver)
        
    def testTravers(self):
        source = OpticalElementSourceGaussian("source")
        source.setX(0)
        source.setY(0)
        source.setZ(0)
        source.setXp(0)
        source.setYp(0)

        source.setSigmaX(23e-06/2.35)
        source.setSigmaY(23e-06/2.35)
        source.setSigmaT(10e-15)
        
        source.setPolarization(LinearHorizontal())
        source.setAveragePhotonEnergy(12400)
        source.setPulseEnergy(0.001)
        source.setRepititionRate(1)
        
        
        space_1 = OpticalElementSpace("space 1")
        space_1.setLength(10.0)
        
        aperture = OpticalElementAperture("aperature")
        aperture.setApertureType(Disc())
        aperture.setDiameter(1.0e-5)
        
        
        space_2 = OpticalElementSpace("space 2")
        space_2.setLength(1.0)

        
        lens = OpticalElementLens("lens")
        lens.setFocalX(1.0)
        lens.setFocalY(1.0)
        
        space_3 = OpticalElementSpace("space 3")
        space_3.setLength(1.0)

        screen = OpticalElementScreen("screen")

        source.addOutput(aperture)
        aperture.addOutput(space_1)
        space_1.addOutput(screen)
        #space_1.addOutput(aperture)
        #aperture.addOutput(space_2)
        #space_2.addOutput(lens)
        #lens.addOutput(space_3)
        #space_3.addOutput(screen)
        
        driver = SRWDriver()

        source.startTravers(driver)
        
        intensity = list(screen.calculateIntensity3D(driver).values())[0]
        my_plot(intensity[0],
                intensity[1],
                intensity[2])
