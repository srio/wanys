"""
Represents polarization.
"""

class Polarization(object):
    def __init__(self, name):
        self.__name = name
        
    def description(self):
        return self.__name
    
    def __eq__(self, candidate):
        return (self.__name == candidate.__name)
    
    def __ne__(self, candidate):
        return not self.__eq__(candidate)
    
    @staticmethod
    def all():
        return [LinearVertical(),
                LinearHorizontal(),
                Linear45Degree(),
                Linear135Degree(),
                CircularRight(),
                CircularLeft()
                ]

class LinearVertical(Polarization):
    def __init__(self):
        Polarization.__init__(self, "Linear vertical")
        
class LinearHorizontal(Polarization):
    def __init__(self):
        Polarization.__init__(self, "Linear horizontal")

class Linear45Degree(Polarization):
    def __init__(self):
        Polarization.__init__(self, "Linear 45 degree")
        
class Linear135Degree(Polarization):
    def __init__(self):
        Polarization.__init__(self, "Linear 135 degree")

class CircularRight(Polarization):
    def __init__(self):
        Polarization.__init__(self, "Circular right")
        
class CircularLeft(Polarization):
    def __init__(self):
        Polarization.__init__(self, "Circular left")
        
        