import numpy as np

from srwlib import *
from orangecontrib.wanys.drivers.srw.Wavefront import SRWWavefront

class SRWAdapter(object):
    def __init__(self):
        self.setSamplingFactor(1)

    def undulator(self, undulator):

        magnetic_fields = []

        if undulator.K_vertical() > 0.0:
            vertical_field = SRWLMagFldH(1, 'v', undulator.B_vertical(), 0, 1, 1)
            magnetic_fields.append(vertical_field)

        if undulator.K_horizontal() > 0.0:
            horizontal_field = SRWLMagFldH(1, 'h', undulator.B_horizontal(), 0, -1, 1)
            magnetic_fields.append(horizontal_field)

        srw_undulator = SRWLMagFldU(magnetic_fields,
                                    undulator.periodLength(),
                                    undulator.periodNumber())

        return srw_undulator

    def magnetFieldFromUndulator(self, undulator):

        srw_undulator = self.undulator(undulator)

        magFldCnt = SRWLMagFldC([srw_undulator],
                                array('d', [0]), array('d', [0]), array('d', [0])) #Container of all Field Elements

        return magFldCnt

    def electronBeam(self, electron_beam, x=0.0, y=0.0 ,xp=0.0, yp=0.0):
        #***********Electron Beam
        srw_electron_beam = SRWLPartBeam()
        srw_electron_beam.Iavg = electron_beam.averageCurrent() #Average Current [A]
        srw_electron_beam.partStatMom1.x = electron_beam.x() #Initial Transverse Coordinates (initial Longitudinal Coordinate will be defined later on) [m]
        srw_electron_beam.partStatMom1.y = electron_beam.y()
        #print("SAMPLED POS", srw_electron_beam.partStatMom1.x, srw_electron_beam.partStatMom1.y)
        srw_electron_beam.partStatMom1.z = 0#electron_beam.z()
        srw_electron_beam.partStatMom1.xp = xp# electron_beam.x_p() #Initial Relative Transverse Velocities
        srw_electron_beam.partStatMom1.yp = yp#electron_beam.y_p()
        srw_electron_beam.partStatMom1.gamma = electron_beam.gamma() #Relative Energy
        #print("SAMPLED GAMMA", srw_electron_beam.partStatMom1.gamma)

        return srw_electron_beam

    def createSRWWavefrontFromSourceGaussian(self, electron_beam, source_gaussian, distance_first_element, first_aperture):

        srw_gaussian_beam    = SRWLGsnBm()

        srw_gaussian_beam.x  = 0
        srw_gaussian_beam.y  = 0
        srw_gaussian_beam.z  = 0 #int(gaussian_beam.z())
        srw_gaussian_beam.xp = 0 # #Average Angles of Gaussian Beam at Waist [rad]source_gaussian.sigmaXPrime()
        srw_gaussian_beam.yp = 0 #source_gaussian.sigmaYPrime()
        energy = int(source_gaussian.energy())
        srw_gaussian_beam.avgPhotEn = energy
        srw_gaussian_beam.pulseEn   = 0.001#gaussian_beam.pulseEnergy()
        srw_gaussian_beam.repRate   = 1#int(gaussian_beam.repititionRate())

        #polarization = gaussian_beam.polarization()
        #if polarization==LinearVertical():
        #    srw_gaussian_beam.polar = 2
        #elif polarization==LinearHorizontal():
        #    srw_gaussian_beam.polar = 1
        #elif polarization==Linear45Degree():
        #    srw_gaussian_beam.polar = 3
        #elif polarization==Linear135Degree():
        #    srw_gaussian_beam.polar = 4
        #elif polarization==CircularRight():
        #    srw_gaussian_beam.polar = 5
        #elif polarization==CircularLeft():
        #    srw_gaussian_beam.polar = 6
        #else:
        #    raise Exception("Polarisation %s not handled." % polarization)
        srw_gaussian_beam.polar = 2

        srw_gaussian_beam.sigX  = source_gaussian.sigmaX()
        srw_gaussian_beam.sigY  = source_gaussian.sigmaY()
        srw_gaussian_beam.sigT  = 10e-15
        srw_gaussian_beam.mx    = 0
        srw_gaussian_beam.my    = 0

        print("FIRST APERTURE", first_aperture)
        print("DISTANCE FIRST ELEMENT", distance_first_element)

        srw_wavefront = self.createQuadraticSRWWavefrontSingleEnergy(1000,0.5*first_aperture, distance_first_element, electron_beam, energy)

        srw_wavefront.partBeam.partStatMom1.x  = srw_gaussian_beam.x #Some information about the source in the Wavefront structure
        srw_wavefront.partBeam.partStatMom1.y  = srw_gaussian_beam.y
        srw_wavefront.partBeam.partStatMom1.z  = srw_gaussian_beam.z
        srw_wavefront.partBeam.partStatMom1.xp = srw_gaussian_beam.xp
        srw_wavefront.partBeam.partStatMom1.yp = srw_gaussian_beam.yp

        sampFactNxNyForProp = 1 #sampling factor for adjusting nx, ny (effective if > 0)
        arPrecPar = [sampFactNxNyForProp]
        #arPrecPar = self.normalPrecisionParameter()

        srwl.CalcElecFieldGaussian(srw_wavefront, srw_gaussian_beam, arPrecPar)

        return srw_wavefront

    def createQuadraticSRWWavefront(self, grid_size, grid_length, z_start, electron_beam, energy_number, energy_start, energy_end):
        return self.createRectangularSRWWavefront(grid_size, grid_length, grid_length, z_start, electron_beam, energy_number, energy_start, energy_end)

    def createFirstQuadrantSRWWavefront(self, grid_size, grid_length, z_start, electron_beam, energy_number, energy_start, energy_end):
        wfr = SRWLWfr()
        wfr.allocate(energy_number, grid_size, grid_size) #Numbers of points vs Photon Energy, Horizontal and Vertical Positions (may be modified by the library!)
        wfr.mesh.zStart = float(z_start)      #Longitudinal Position [m] at which SR has to be calculated
        wfr.mesh.eStart = energy_start        #1090. #Initial Photon Energy [eV]
        wfr.mesh.eFin   = energy_end          #1090. #Final Photon Energy   [eV]
        wfr.mesh.xStart = 0.0                 #Initial Horizontal Position  [m]
        wfr.mesh.xFin   =  grid_length        #Final Horizontal Position    [m]
        wfr.mesh.yStart = 0.0                 #Initial Vertical Position    [m]
        wfr.mesh.yFin   =  grid_length        #Final Vertical Position      [m]

        wfr.partBeam = self.electronBeam(electron_beam)

        return wfr

    def createRectangularSRWWavefront(self, grid_size, grid_length_x, grid_length_y , z_start, electron_beam, energy_number, energy_start, energy_end, xp=0.0, yp=0.0):
        wfr = SRWLWfr()
        wfr.allocate(energy_number, grid_size, grid_size) #Numbers of points vs Photon Energy, Horizontal and Vertical Positions (may be modified by the library!)
        wfr.mesh.zStart = float(z_start)        #Longitudinal Position [m] at which SR has to be calculated
        wfr.mesh.eStart = energy_start          #1090. #Initial Photon Energy [eV]
        wfr.mesh.eFin   = energy_end            #1090. #Final Photon Energy   [eV]
        wfr.mesh.xStart = -grid_length_x        #Initial Horizontal Position  [m]
        wfr.mesh.xFin   =  grid_length_x        #Final Horizontal Position    [m]
        wfr.mesh.yStart = -grid_length_y        #Initial Vertical Position    [m]
        wfr.mesh.yFin   =  grid_length_y        #Final Vertical Position      [m]

        wfr.partBeam = self.electronBeam(electron_beam, xp=xp, yp=yp)

        return wfr

    def createQuadraticSRWWavefrontSingleEnergy(self, grid_size, grid_length, z_start, electron_beam, energy):
        return self.createQuadraticSRWWavefront(grid_size,grid_length, z_start, electron_beam,1,energy,energy)

    def createBeamlineOneToOneSourceImage(self,wfr):
        #***********Optical Elements and Propagation Parameters
        fx = wfr.mesh.zStart/2               #Lens focal lengths
        fy = wfr.mesh.zStart/2
        optLens = SRWLOptL(fx, fy)           #Lens
        optDrift = SRWLOptD(wfr.mesh.zStart) #Drift space

        propagParLens = [1, 1, 1., 0, 0, 1., 1., 1., 1., 0, 0, 0]
        propagParDrift = [1, 1, 1., 0, 0, 2., 2., 2., 2., 0, 0, 0]
        #Wavefront Propagation Parameters:
        #[0]: Auto-Resize (1) or not (0) Before propagation
        #[1]: Auto-Resize (1) or not (0) After propagation
        #[2]: Relative Precision for propagation with Auto-Resizing (1. is nominal)
        #[3]: Allow (1) or not (0) for semi-analytical treatment of the quadratic (leading) phase terms at the propagation
        #[4]: Do any Resizing on Fourier side, using FFT, (1) or not (0)
        #[5]: Horizontal Range modification factor at Resizing (1. means no modification)
        #[6]: Horizontal Resolution modification factor at Resizing
        #[7]: Vertical Range modification factor at Resizing
        #[8]: Vertical Resolution modification factor at Resizing
        #[9]: Type of wavefront Shift before Resizing (not yet implemented)
        #[10]: New Horizontal wavefront Center position after Shift (not yet implemented)
        #[11]: New Vertical wavefront Center position after Shift (not yet implemented)
        optical_beamline = SRWLOptC([optLens, optDrift],
                                    [propagParLens, propagParDrift]) #"Beamline" - Container of Optical Elements (together with the corresponding wavefront propagation instructions)

        return optical_beamline

    def setSamplingFactor(self, sampling_factor):
        self._sampling_factor = sampling_factor

    def samplingFactor(self):
        return self._sampling_factor

    def normalPrecisionParameter(self):
        #***********Precision Parameters for SR calculation
        meth        = 1 #SR calculation method: 0- "manual", 1- "auto-undulator", 2- "auto-wiggler"
        relPrec     = 0.01 #relative precision
        zStartInteg = 0 #longitudinal position to start integration (effective if < zEndInteg)
        zEndInteg   = 0 #longitudinal position to finish integration (effective if > zStartInteg)
        npTraj      = 20000 #Number of points for trajectory calculation
        useTermin   = 1 #Use "terminating terms" (i.e. asymptotic expansions at zStartInteg and zEndInteg) or not (1 or 0 respectively)
        sampFactNxNyForProp = 3 #sampling factor for adjusting nx, ny (effective if > 0)
        sampFactNxNyForProp = self.samplingFactor() #sampling factor for adjusting nx, ny (effective if > 0)
        arPrecPar = [meth, relPrec, zStartInteg, zEndInteg, npTraj, useTermin, sampFactNxNyForProp]

        return arPrecPar

    def wavefront(self, electron_beam, undulator, z_start, max_theta_x, max_theta_y, energy_number, energy_start, energy_end, xp=0.0, yp=0.0):

        grid_length_x = max_theta_x * z_start / sqrt(2.0)
        grid_length_y = max_theta_y * z_start / sqrt(2.0)

        return self.wavefrontByCoordinates(electron_beam, undulator, z_start,
                                           grid_length_x, grid_length_y,
                                           energy_number, energy_start, energy_end, xp, yp)

    def wavefrontByCoordinates(self, electron_beam, undulator, z_start, grid_length_x, grid_length_y, energy_number, energy_start, energy_end, xp=0.0, yp=0.0):

        if isinstance(undulator, SRWLMagFldC):
            print("Using SRW magnet field container object directly!")
            magnetic_field = undulator
        else:
            magnetic_field = self.magnetFieldFromUndulator(undulator)

        wfr = self.createRectangularSRWWavefront(grid_size=100,
                                                 grid_length_x=grid_length_x,
                                                 grid_length_y=grid_length_y,
                                                 z_start=z_start,
                                                 electron_beam=electron_beam,
                                                 energy_number=energy_number,
                                                 energy_start=energy_start,
                                                 energy_end=energy_end,
                                                 xp=xp,
                                                 yp=yp)


        precision_parameter = self.normalPrecisionParameter()

        #**********************Calculation (SRWLIB function calls) and post-processing
        print('   >> Using grid of: NX: %d   NY: %d '%(SRWWavefront(wfr).dim_x(), SRWWavefront(wfr).dim_y()))
        print('   Performing Initial Electric Field calculation with SRW... ')
        srwl.CalcElecFieldSR(wfr, 0, magnetic_field, precision_parameter)
        print('   >> Returned grid of: NX: %d   NY: %d '%(SRWWavefront(wfr).dim_x(), SRWWavefront(wfr).dim_y()))
        print('done')

        return SRWWavefront(wfr)

    def wavefrontForSingleEnergy(self, electron_beam, undulator, z_start, max_theta, energy):
        return self.wavefront(electron_beam, undulator, z_start, max_theta, max_theta, 1, energy, energy)

    def wavefrontRectangularForSingleEnergy(self, electron_beam, undulator, z_start, max_theta_x, max_theta_y, energy,xp=0.0, yp=0.0):
        return self.wavefront(electron_beam, undulator, z_start, max_theta_x, max_theta_y, 1, energy, energy, xp, yp)


    def SRWWavefrontFromWavefront(self, wavefront, Rx, dRx, Ry, dRy):
        wavefront = wavefront.asEvenGridpointsGrid()
        s = wavefront.E_field_as_numpy()[0,:,:,0].size

        r_horizontal_field = wavefront.E_field_as_numpy()[0,:,:,0].real.transpose().flatten().astype(np.float)
        i_horizontal_field = wavefront.E_field_as_numpy()[0,:,:,0].imag.transpose().flatten().astype(np.float)

        tmp = np.zeros(s * 2, dtype=np.float32)
        for i in range(s):
            tmp[2*i]=r_horizontal_field[i]
            tmp[2*i+1]=i_horizontal_field[i]

        horizontal_field = array('f', tmp)

        r_vertical_field = wavefront.E_field_as_numpy()[0,:,:,1].real.transpose().flatten().astype(np.float)
        i_vertical_field = wavefront.E_field_as_numpy()[0,:,:,1].imag.transpose().flatten().astype(np.float)

        tmp = np.zeros(s * 2, dtype=np.float32)
        for i in range(s):
            tmp[2*i]=r_vertical_field[i]
            tmp[2*i+1]=i_vertical_field[i]

        vertical_field = array('f', tmp)

        srw_wavefront = SRWLWfr(_arEx=horizontal_field,
                                _arEy=vertical_field,
                                _typeE='f',
                                _eStart=float(wavefront.energies().min()),
                                _eFin=float(wavefront.energies().max()),
                                _ne=wavefront.numberEnergies(),
                                _xStart=float(wavefront.x_start()),
                                _xFin=float(wavefront.x_end()),
                                _nx=wavefront.dim_x(),
                                _yStart=float(wavefront.y_start()),
                                _yFin=float(wavefront.y_end()),
                                _ny=wavefront.dim_y(),
                                _zStart=float(wavefront.z()))

        srw_wavefront.Rx = Rx
        srw_wavefront.Ry = Ry
        srw_wavefront.dRx = dRx
        srw_wavefront.dRy = dRy

        return srw_wavefront

    def propagate(self, wavefront, Rx, dRx, Ry, dRy, z):

        if z>=0.0:
            wfr = self.SRWWavefrontFromWavefront(wavefront, Rx, dRx, Ry, dRy)
            optBL = SRWLOptC([SRWLOptD(z)],
                             [[1,  1, 3.0,  0,  0, 1.0, 1.0, 1.0, 1.0,  0,  0,   0]])
            srwl.PropagElecField(wfr, optBL)

            propagated_wavefront = SRWWavefront(wfr).toNumpyWavefront()
        else:
            wavefront.conjugate()
            wfr = self.SRWWavefrontFromWavefront(wavefront, Rx, dRx, Ry, dRy)
            optBL = SRWLOptC([SRWLOptD(-z)],
                             [[1,  0, 2.0,  0,  0, 1.0, 1.0, 1.0, 1.0,  0,  0,   0]])
            srwl.PropagElecField(wfr, optBL)
            wavefront.conjugate()
            propagated_wavefront = SRWWavefront(wfr).toNumpyWavefront()
            propagated_wavefront.conjugate()

        return propagated_wavefront

    def propagateToSourcePlane(self, wavefront, Rx, dRx, Ry, dRy):
        return self.propagate(wavefront, Rx, dRx, Ry, dRy, -wavefront.z()/2.0)
