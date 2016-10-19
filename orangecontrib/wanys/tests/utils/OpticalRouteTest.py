"""
Test for optical route.
"""
import unittest
from orangecontrib.wanys.util.OpticalRoute import OpticalRoute
from orangecontrib.wanys.util.OpticalElementLens import OpticalElementLens
from orangecontrib.wanys.util.OpticalElementSourceGaussian import OpticalElementSourceGaussian

class OpticalRouteTest(unittest.TestCase):
    def testConstructor(self):
        optical_route = OpticalRoute()
        
        self.assertIsInstance(optical_route,
                              OpticalRoute)
        
    def testAddElement(self):
        optical_route = OpticalRoute()
        optical_route.addElement(OpticalElementSourceGaussian("source"))
        optical_route.addElement(OpticalElementLens("lens"))

        route = optical_route.route()
        self.assertIsInstance(route[0],
                              OpticalElementSourceGaussian)
        self.assertEqual(route[0].name(),
                         "source")
        
        self.assertIsInstance(route[1],
                              OpticalElementLens)
        self.assertEqual(route[1].name(),
                         "lens")


    def testHash(self):
        return
        
    def testClone(self):
        return
    