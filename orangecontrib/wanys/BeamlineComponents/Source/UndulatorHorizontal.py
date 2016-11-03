from BeamlineComponents.Source.Undulator import Undulator

class UndulatorHorizontal(Undulator):
    def __init__(self, K, period_length, period_number):

        Undulator.__init__(self,
                           K_vertical=0.0,
                           K_horizontal=K,
                           period_length=period_length,
                           periods_number=period_number)

    def K(self):
            K = self.K_horizontal()

    def B(self):
        return self._magneticFieldStrengthFromK(self.K())
