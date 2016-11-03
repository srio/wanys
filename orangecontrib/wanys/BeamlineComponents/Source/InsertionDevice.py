from numpy import pi
import scipy.constants.codata

class InsertionDevice(object):
    def __init__(self, K_vertical, K_horizontal, period_length, periods_number):
        self._K_vertical = K_vertical
        self._K_horizontal = K_horizontal
        self._period_length = period_length
        self._periods_number = periods_number

    def periodLength(self):
        return self._period_length

    def periodNumber(self):
        return self._periods_number

    def length(self):
        return self.periodNumber() * self.periodLength()

    def K_vertical(self):
        return self._K_vertical

    def K_horizontal(self):
        return self._K_horizontal

    def _magneticFieldStrengthFromK(self, K):
        codata = scipy.constants.codata.physical_constants
        speed_of_light = codata["speed of light in vacuum"][0]
        mass_electron = codata["electron mass"][0]
        elementary_charge=codata["elementary charge"][0]

        B = K * 2 * pi * mass_electron * speed_of_light / (elementary_charge * self.periodLength())

        return B

    def B_vertical(self):
        return self._magneticFieldStrengthFromK(self.K_vertical())

    def B_horizontal(self):
        return self._magneticFieldStrengthFromK(self.K_horizontal())