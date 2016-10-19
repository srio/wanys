import unittest

import numpy as np

from orangecontrib.srw.interfaces.coherence.autocorrelation.SigmaMatrix import SigmaWaist
from orangecontrib.srw.interfaces.coherence.autocorrelation import PhaseSpaceDensity


def rho_r(f, sigma_x, sigma_y, r_x, r_y):
    f_x = np.exp(-0.5 * (r_x/sigma_x) ** 2)
    f_y = np.exp(-0.5 * (r_y/sigma_y) ** 2)

    for i_x in range(f.shape[0]):
        f[i_x,:] = f_x[i_x] * f_y

    f *= 1.0 / (2 * np.pi * sigma_x * sigma_y)


class PhaseSpaceDensityTest(unittest.TestCase):
    def testConstructor(self):
        sigma_matrix = SigmaWaist(sigma_x=0.945 * 10**-4,
                                            sigma_y=0.01860 * 10**-4,
                                            sigma_x_prime=0.025* 10**-4,
                                            sigma_y_prime=0.0075* 10**-4)

        density = PhaseSpaceDensity(sigma_matrix,0)
        self.assertIsInstance(density, PhaseSpaceDensity)
