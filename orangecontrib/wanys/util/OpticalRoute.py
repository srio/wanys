"""
Route of optical elements taken.
"""
import copy

class OpticalRoute(object):
    def __init__(self):
        self.__route = ()
        
    def addElement(self, element):
        self.__route = self.__route + (element,)
        
    def route(self):
        return copy.copy(self.__route)

    def __hash__(self):
        return hash(self.__route)

    def __eq__( self, other ):
        return self.__route == other.__route

    def __ne__( self, other ):
        return not self.__eq__(other)
        
    def clone(self):
        return copy.copy(self)
    