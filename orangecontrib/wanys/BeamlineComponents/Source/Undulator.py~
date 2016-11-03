from numpy import pi, sqrt
import scipy.constants.codata

from BeamlineComponents.Source.InsertionDevice import InsertionDevice

class Undulator(InsertionDevice):

    def __init__(self, K_vertical, K_horizontal, period_length, periods_number):
        InsertionDevice.__init__(self, K_vertical, K_horizontal, period_length, periods_number)

    def resonanceWavelength(self, gamma, theta_x, theta_z):
        wavelength = (self.periodLength() / (2.0*gamma **2)) * \
                     (1 + self.K_vertical()**2 / 2.0 + self.K_horizontal()**2 / 2.0 + \
                      gamma**2 * (theta_x**2 + theta_z ** 2))
        return wavelength

    def resonanceFrequency(self, gamma, theta_x, theta_z):
        codata = scipy.constants.codata.physical_constants
        speed_of_light = codata["speed of light in vacuum"][0]

        frequency = speed_of_light / self.resonanceWavelength(gamma, theta_x, theta_z)
        return frequency

    def resonanceEnergy(self, energy_in_GeV, theta_x, theta_y):
        codata = scipy.constants.codata.physical_constants
        energy_in_ev = codata["Planck constant"][0] * self.resonanceFrequency(energy_in_GeV/0.51099890221e-03, theta_x, theta_y) / codata["elementary charge"][0]
        print("Resonance energy", energy_in_ev)
        return energy_in_ev

    def gaussianEstimateDivergence(self, gamma, n=1):
        return (1/(2.0*gamma))*sqrt((1.0/(n*self.periodNumber())) * (1.0 + self.K_horizontal()**2/2.0 + self.K_vertical()**2/2.0))

    def gaussianEstimateBeamSize(self, gamma, n=1):
        return (2.740/(4.0*pi))*sqrt(self.periodLength()*self.resonanceWavelength(gamma,0.0,0.0)/n)

    def maximalAngularFluxEnergy(self):
        return self.resonanceEnergy*(1.0-1.0/float(self.periodNumber()))
