"""
Represents an elliptical aperture.
"""

class ApertureEllipse(object):
    def __init__(self, axis_a, axis_b):
        self._axis_a = axis_a
        self._axis_b = axis_b

    def axisA(self):
        return self._axis_a

    def axisB(self):
        return self._axis_b
