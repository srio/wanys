"""
Represents an optical square source.
"""

from BeamlineComponents.Source.SourceRectangle import SourceRectangle

class SourceSquare(SourceRectangle):
    def __init__(self, length_side):
        SourceRectangle.__init__(length_side)

    def lengthSide(self):
        return self.lengthVertical()
