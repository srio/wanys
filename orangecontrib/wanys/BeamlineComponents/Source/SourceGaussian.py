"""
Represents an optical Gaussian source.
"""

class SourceGaussian(object):
    def __init__(self, sigma_x, sigma_y, sigma_x_prime, sigma_y_prime, energy):
        self._sigma_x = sigma_x
        self._sigma_y = sigma_y
        self._sigma_x_prime = sigma_x_prime
        self._sigma_y_prime = sigma_y_prime
        self._energy = energy

    def setAveragePhotonEnergy(self, average_photon_energy):
        self.__average_photon_energy = average_photon_energy
    
    def averagePhotonEnergy(self):
        return self.__average_photon_energy

    def setPulseEnergy(self, pulse_energy):
        self.__pulse_energy = pulse_energy 
    
    def pulseEnergy(self):
        return self.__pulse_energy
    
    def setRepititionRate(self, repitition_rate):
        self.__repitition_rate = repitition_rate

    def repititionRate(self):
        return self.__repitition_rate

    def setPolarization(self, polarization):
        self.__polarization = polarization
        
    def polarization(self):
        return self.__polarization

    def sigmaX(self):
        return self._sigma_x

    def sigmaY(self):
        return self._sigma_y

    def sigmaXPrime(self):
        return self._sigma_x_prime

    def sigmaYPrime(self):
        return self._sigma_y_prime

    def energy(self):
        return self._energy
