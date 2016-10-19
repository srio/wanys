"""
Represents an optical beam.
"""

class OpticalBeam(object):
    def __init__(self, sender):
        self.__sender = sender

    def sender(self):
        return self.__sender