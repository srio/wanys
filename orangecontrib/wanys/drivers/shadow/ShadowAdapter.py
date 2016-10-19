import numpy as np

import Shadow
import Shadow.ShadowTools as st

class ShadowAdapter(object):
    def shadowSourceFromSourceGaussian(self, source_gaussian):
        source = Shadow.Source()

        # TODO: FIX!!!
        source.FDISTR = 3
        source.HDIV1 = 1.0
        source.HDIV2 = 1.0
        source.VDIV1 = 1.0
        source.VDIV2 = 1.0
        source.F_PHOT = 0

        source.NPOINT = source_gaussian._optical_element.driverSettings().valueByName("Number of rays")

        source.SIGMAX = source_gaussian.sigmaX()
        source.SIGMAZ = source_gaussian.sigmaY()
        source.SIGDIX = source_gaussian.sigmaXPrime()
        source.SIGDIZ = source_gaussian.sigmaYPrime()
        source.PH1 = source_gaussian.energy()

        return source

    def intensityFromBeam(self, beam):
        st.plotxy(beam,1,3)

        # return value is expected to be [z(x,y),x,y]
        intensity = [np.arange(9).reshape((3,3)), np.array([0.0,1.0,2.0]), np.array([0.0,1.0,2.0])]

        return intensity

    def phaseFromBeam(self, beam):

        # return value is expected to be [z(x,y),x,y]
        phase = [np.arange(9).reshape((3,3)), np.array([0.0,1.0,2.0]), np.array([0.0,1.0,2.0])]

        return phase
