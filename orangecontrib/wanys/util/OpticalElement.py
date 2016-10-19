"""
Base class for optical element, i.e. mirror, lens,...
"""
from orangecontrib.wanys.util.OpticalRoute import OpticalRoute

class OpticalElement(object):
    def __init__(self, element_typename):

        self.setElementTypename(element_typename)

        self._inputs = []
        self._outputs = []

        self._stored_data = {}

        self.setName("")

        self.setDriverSettings(None)

        self.setOnSynchronize(None)
        self.setOnCalculationStart(None)
        self.setOnCalculationFinished(None)

        self.setBeamlineComponent(None)

    def setBeamlineComponent(self, beamline_component):
        self._beamline_component = beamline_component

    def beamlineComponent(self):
        return self._beamline_component

    def addInput(self, new_input):
        # TODO: Check for cycles
        if new_input in self._inputs:
            return

        self._inputs.append(new_input)
        new_input.addOutput(self)

    def inputs(self):
        return self._inputs

    def removeInput(self, an_input):
        self._inputs.remove(an_input)

    def addOutput(self, new_output):
        # TODO : Check for cycles
        if new_output in self._outputs:
            return

        self._outputs.append(new_output)
        new_output.addInput(self)

    def outputs(self):
        return self._outputs

    def removeOutput(self, output):
        self._outputs.remove(output)

    def _saveDataByRoute(self, route, data):
        self._stored_data[route] = data

    def _dataByRoute(self, route):
        return self._stored_data[route]

    def _hasDataByRoute(self, route):
        return (route in self._stored_data)

    def setElementTypename(self, element_typename):
        self.__element_typename = element_typename

    def elementTypename(self):
        return self.__element_typename

    def setName(self, name):
        self.__name = name

    def name(self):
        return self.__name

    def setTag(self, tag):
        self.__tag = tag

    def tag(self):
        return self.__tag

    def shortInfo(self):
        short_info = self.name()

        return short_info

    def _calculateData(self, route, driver, in_data):

        # Check if data is already stored
        if self._hasDataByRoute(route):
            cached_data = self._dataByRoute(route)
            # Check if stored data is good or needs recalculation.
            if(driver.isDataUpToDate(self, in_data, cached_data)):
                return cached_data

        # Calculate the data.
        out_data = driver.calculateData(self, in_data)

        # Save/cache the output data.
        self._saveDataByRoute(route, out_data)

        return out_data

    def startTravers(self, driver):
        route = OpticalRoute()
        self._continueTravers(route, driver, in_data=None)

    def _continueTravers(self, route, driver, in_data):
        my_route = route.clone()
        my_route.addElement(self)

        self._raiseSynchronize()
        self._raiseCalculationStart()
        out_data = self._calculateData(my_route, driver, in_data)
        self._raiseCalculationFinished()
        for output in self.outputs():
            print("travers ", output.name())
            output._continueTravers(my_route, driver, out_data)

    def setOnCalculationFinished(self, on_calculation_finished):
        self.__on_calculation_finished = on_calculation_finished

    def _raiseCalculationFinished(self):
        if self.__on_calculation_finished is not None:
            self.__on_calculation_finished()

    def setOnCalculationStart(self, on_calculation_start):
        self.__on_calculation_start = on_calculation_start

    def _raiseCalculationStart(self):
        if self.__on_calculation_start is not None:
            self.__on_calculation_start()

    def setOnSynchronize(self, on_synchronize):
        self.__on_synchronize = on_synchronize

    def _raiseSynchronize(self):
        if self.__on_synchronize is not None:
            self.__on_synchronize()

    def findSources(self):
        # If source node, return self.
        if self.inputs() == []:
            return [self]

        # If not source node recursively traverse.
        sources = []
        for an_input in self.inputs():
            sources = sources + an_input.findSources()

        return sources

    def setDriverSettings(self, driver_settings):
        self.__driver_settings = driver_settings

    def driverSettings(self):
        return self.__driver_settings
