"""
Represents an optical screen.
"""
from orangecontrib.wanys.util.OpticalElement import OpticalElement

class OpticalElementScreen(OpticalElement):
    def __init__(self, name):
        OpticalElement.__init__(self, "Screen" + name)

    def calculateIntensityHorizontalCut(self, driver, horizontal_coordinate):
        """
        Calculates a horizontal intensity cut.
        """
        result = {}
        for key in list(self._stored_data.keys()):
            in_data = self._dataByRoute(key)
            result[key] = driver.calculateIntensityHorizontalCut(in_data, horizontal_coordinate)

        return result

    def calculateIntensityVerticalCut(self, driver, vertical_coordinate):
        """
        Calculates a vertical intensity cut.
        """
        result = {}
        for key in list(self._stored_data.keys()):
            in_data = self._dataByRoute(key)
            result[key] = driver.calculateIntensityVerticalCut(in_data, vertical_coordinate)

        return result

    def calculateIntensity3D(self, driver):
        result = {}
        print("OE SCREEN:", list(self._stored_data.keys()))
        for key in list(self._stored_data.keys()):
            in_data = self._dataByRoute(key)
            result[key] = driver.calculateIntensity3D(in_data)
        
        return result

    def calculatePhase3D(self, driver):
        result = {}
        for key in list(self._stored_data.keys()):
            in_data = self._dataByRoute(key)
            result[key] = driver.calculatePhase3D(in_data)
        
        return result
