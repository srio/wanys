"""
Represents an ideal lens.
"""


class LensIdeal(object):
    def __init__(self, focal_x, focal_y):
        self._focal_x = focal_x
        self._focal_y = focal_y

    def focalX(self): 
        return self._focal_x

    def focalY(self):
        return self._focal_y