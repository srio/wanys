"""
Represents a square aperture.
"""

from BeamlineComponents.Aperture.ApertureRectangle import ApertureRectangle

class ApertureSquare(ApertureRectangle):
    def __init__(self, side_length):
        AperatureRectangle.__init__(self, side_length, side_length)

    def sideLength(self):
        return self.lengthVertical()
