import numpy

class ProbabiltyDistribution(object):
    def __init__(self, probability_density):
        self._probability_density = probability_density

    def density(self):
        return self._probability_density

    def sample(self):
        raise Exception("Must override.")

class DiscreteDistribution(ProbabiltyDistribution):
    def __init__(self, values, probabilties):
        self._values = numpy.array(values)
        self._probabilites  = numpy.array(probabilties)

        ProbabiltyDistribution.__init__(self, self._discrete_propability_density)

    def _discrete_propability_density(self, x):
        norm = numpy.sum(self._values)

        c = 0.0
        for value, probabilty in zip(self._values, self._probabilites):
            c = c + probabilty
            if c >= x:
                return value

        return self._values[-1]

    def sample(self):
        random_number = numpy.random.rand(1)[0]
        value = self._probability_density(random_number)
        return value


class DeltaDistribution(DiscreteDistribution):
    def __init__(self, value):
        DiscreteDistribution.__init__(self,[value],[1.0])

class NormalDistribution(ProbabiltyDistribution):
    def __init__(self, mean, sigma, norm):
        self._norm = norm
        self._mean = mean
        self._sigma = sigma

        f = lambda x: norm * (1.0/numpy.sqrt(2.0*numpy.pi * sigma**2)) * numpy.exp(-(x-mean)**2 / (2.0*sigma**2))
        ProbabiltyDistribution.__init__(self, f)

    def norm(self):
        return self._norm

    def mean(self):
        return self._mean

    def sigma(self):
        return self._sigma

    def sample(self):
        value =  self.norm() * numpy.random.normal(loc = self.mean(),scale = self.sigma())
        return value
