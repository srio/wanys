"""
Represents an optical rectangular source.
"""

class SourceRectangular(object):
    def __init__(self, length_vertical, length_horizontal):
        self._length_vertical = length_vertical
        self._length_horizontal = length_horizontal

    def lengthVertical(self):
        return self._length_vertical

    def lengthHorizontal(self):
        return self._length_horizontal