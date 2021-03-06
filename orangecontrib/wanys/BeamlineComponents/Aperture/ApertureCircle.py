"""
Represents a circular aperture.
"""

from orangecontrib.wanys.BeamlineComponents.Aperture.ApertureEllipse import ApertureEllipse

class ApertureCircle(ApertureEllipse):
    def __init__(self, diameter):
        ApertureEllipse.__init__(self, diameter, diameter)

    def diameter(self):
        return self.axisA()
