"""
Test for Optical elements
"""
import unittest
from orangecontrib.wanys.util.OpticalElement import OpticalElement
from orangecontrib.wanys.util.OpticalRoute import OpticalRoute

class OpticalElementMock(OpticalElement):
    def __init__(self, name):
        OpticalElement.__init__(self, "Mock element", name)

def getOpticalElements(number):
    result = []

    for i in range(number):
        result.append(OpticalElementMock("test%i" % i))

    return result

class OpticalElementTest(unittest.TestCase):
    def testConstructor(self):
        optical_element = OpticalElementMock("test1")

        self.assertIsInstance(optical_element, OpticalElement)
        self.assertEqual(optical_element.name(),
                         "test1")

    def testInput(self):
        optical_element = getOpticalElements(3)

        optical_element[0].addOutput(optical_element[1])
        optical_element[1].addOutput(optical_element[2])

        # Inputs
        self.assertEqual(optical_element[0].inputs(),
                         [])
        self.assertEqual(optical_element[1].inputs(),
                         [optical_element[0]])

        self.assertEqual(optical_element[2].inputs(),
                         [optical_element[1]])

        # Outputs
        self.assertEqual(optical_element[0].outputs(),
                         [optical_element[1]])
        self.assertEqual(optical_element[1].outputs(),
                         [optical_element[2]])        

        self.assertEqual(optical_element[2].outputs(),
                         [])

    def testOutput(self):
        optical_element = getOpticalElements(3)

        optical_element[0].addInput(optical_element[1])
        optical_element[1].addInput(optical_element[2])

        # Outputs
        self.assertEqual(optical_element[0].outputs(),
                         [])
        self.assertEqual(optical_element[1].outputs(),
                         [optical_element[0]])

        self.assertEqual(optical_element[2].outputs(),
                         [optical_element[1]])

        # Inputs
        self.assertEqual(optical_element[0].inputs(),
                         [optical_element[1]])
        self.assertEqual(optical_element[1].inputs(),
                         [optical_element[2]])

        self.assertEqual(optical_element[2].inputs(),
                         [])
        
    def testSaveDataByRoute(self):
        optical_element = getOpticalElements(3)

        route_1 = OpticalRoute()
        route_1.addElement(optical_element[0])
        route_1.addElement(optical_element[1])

        route_2 = route_1.clone()
        route_2.addElement(optical_element[2])
        
        data_1 = ("abc","123","DEF")
        data_2 = ("-213","123","XYZ")

        optical_element[0]._saveDataByRoute(route_1, data_1)
        optical_element[0]._saveDataByRoute(route_2, data_2)
        
        self.assertEqual(optical_element[0]._dataByRoute(route_1), 
                         data_1)

        self.assertEqual(optical_element[0]._dataByRoute(route_2), 
                         data_2)
       
    def testDataByRoute(self):
        optical_element = getOpticalElements(2)

        route = OpticalRoute()
        route.addElement(optical_element[0])
        route.addElement(optical_element[1])
        
        data = ("abc","123","DEF")

        optical_element[0]._saveDataByRoute(route, data)
        
        self.assertEqual(optical_element[0]._dataByRoute(route), 
                         data)

    def testHasDataByRoute(self):
        optical_element = getOpticalElements(3)

        route_1 = OpticalRoute()
        route_1.addElement(optical_element[0])
        route_1.addElement(optical_element[1])

        route_2 = route_1.clone()
        route_2.addElement(optical_element[2])
        
        data = ("abc","123","DEF")

        optical_element[0]._saveDataByRoute(route_2, data)
        
        self.assertTrue(optical_element[0]._hasDataByRoute(route_2))
        self.assertFalse(optical_element[0]._hasDataByRoute(route_1))

    
    def testSetAndGetElementTypename(self):
        optical_element = OpticalElementMock("mock")
        
        optical_element.setElementTypename("typename")
        self.assertEqual(optical_element.elementTypename(),
                         "typename")

    def testSetName(self):
        optical_element = OpticalElementMock("mock")
        
        optical_element.setName("name")
        self.assertEqual(optical_element.name(),
                         "name")

    def name(self):
        optical_element = OpticalElementMock("mock")
        
        self.assertEqual(optical_element.name(),
                         "mock")
    
    def testSetAndGetTag(self):
        optical_element = OpticalElementMock("mock")
        
        optical_element.setTag("tag")
        self.assertEqual(optical_element.tag(),
                         "tag")
    
    def testShortInfo(self):
        optical_element = OpticalElementMock("mock")

        self.assertEqual(optical_element.shortInfo(),
                         optical_element.name())

    def testFindSources(self):
        optical_element = getOpticalElements(3)

        optical_element[0].addOutput(optical_element[1])
        optical_element[1].addOutput(optical_element[2])

        self.assertEqual(optical_element[2].findSources(),
                         [optical_element[0]])

        self.assertEqual(optical_element[1].findSources(),
                         [optical_element[0]])

        self.assertEqual(optical_element[0].findSources(),
                         [optical_element[0]])

        optical_source = OpticalElementMock("extra source")

        optical_element[1].addInput(optical_source)
        self.assertEqual(optical_element[1].findSources(),
                         [optical_element[0], optical_source])

        self.assertEqual(optical_element[2].findSources(),
                         [optical_element[0], optical_source])
