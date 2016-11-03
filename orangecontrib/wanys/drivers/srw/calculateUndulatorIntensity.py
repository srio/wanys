import mpi4py.MPI as mpi

from orangecontrib.wanys.BeamlineComponents.Source.UndulatorVertical import UndulatorVertical
from orangecontrib.wanys.BeamlineComponents.Beam.ElectronBeam import ElectronBeam
from SRWAdapter import SRWAdapter
from Intensities import Intensities
from orangecontrib.wanys.util.ProbabilityDistributions import NormalDistribution
from orangecontrib.wanys.interfaces.coherence.math.Gradienter import WavefrontGradient


def convolveWavefront(my_wavefront):
    transverse_x_distribution = NormalDistribution(mean=0.0, sigma=0.00005,norm=1.0)
    transverse_y_distribution = NormalDistribution(mean=0.0, sigma=0.000001,norm=1.0)

    my_wavefront = my_wavefront.toNumpyWavefront()
#    my_wavefront.extend(-0.0002, 0.0002, -0.0002, 0.0002)

    k = lambda x,y: transverse_x_distribution.density()(x) * transverse_y_distribution.density()(y)
    my_wavefront = my_wavefront.convolve(k)

    return my_wavefront

def addWavefrontIntensity(my_wavefront, energy, intensities):
    y_index=int(my_wavefront.dim_y()/2)
    x_intensity = my_wavefront.intensity_at_y(y_index)
    y_coordinates = my_wavefront.absolute_y_coordinates()

    x_index=int(my_wavefront.dim_x()/2)
    y_intensity = my_wavefront.intensity_at_x(x_index)
    x_coordinates = my_wavefront.absolute_x_coordinates()

    intensity_plane = my_wavefront.intensity_plane()[0,:,:]

    intensities.addHorizontalCut(energy, x_coordinates, x_intensity)
    intensities.addVerticalCut(energy, y_coordinates, y_intensity)

    #intensity_plane = pywt.dwt2(intensity_plane, "sym4")[0]
    #intensity_plane = numpy.fft.fft2(intensity_plane).imag
    #x_coordinates=range(intensity_plane.shape[0])
    #y_coordinates=range(intensity_plane.shape[1])

    intensities.addPlane(energy, x_coordinates, y_coordinates, intensity_plane)

def calcualteIntensitiesForEnergiesAndElectronBeams(undulator, energies, beams):

    adapter = SRWAdapter()
    intensities = Intensities()

    comm = mpi.COMM_WORLD
    rank = comm.Get_rank()

    max_theta = undulator.gaussianCentralConeDivergence(beams[0].gamma()) * 2.5

    for index, energy in enumerate(energies):
        print("Calculating energy %f %i of %i" %(energy, index+1, len(energies)))
        my_wavefront = None
        longitudinal_z_distribution = NormalDistribution(mean=0.0, sigma=0.0005,norm=1.0)
        wavefronts=[]
        for electron_beam in beams:
            for i in range(2):
                if(i%comm.Get_size() != rank):
                    continue

                print("%i, Calculating electron %i of %i" %(rank,i,electron_beam.electrons()))

                z = 20.0 - i#longitudinal_z_distribution.sample()
                calc_wavefront = adapter.wavefrontForSingleEnergy(electron_beam,undulator, z,
                                                                  max_theta,
                                                                  energy)
                if my_wavefront is None:
                    my_wavefront = calc_wavefront
                else:
                    my_wavefront = my_wavefront.add(calc_wavefront)
                wavefronts.append(my_wavefront)

        g = WavefrontGradient()
        grad = g.wavefrontGradient(wavefronts[0], wavefronts[1])

        my_wavefront = wavefronts[0].toNumpyWavefront()
        my_wavefront._e_field=grad
       # shift_wavefront.shiftOrigin(69, 0)
       # my_wavefront = my_wavefront.mul(shift_wavefront)

        print("scal", my_wavefront._e_field.sum())

        print("%i waits for other tasks" % rank)

        comm.barrier()
        if comm.Get_size() > 1:
            for id_rank in range(1,comm.Get_size()):
                if rank == 0:
                    recved_wavefront  = comm.recv(source=id_rank, tag=11)
                    print("%i adds wavefront" % rank)
                    my_wavefront = my_wavefront.add(recved_wavefront)
                elif rank == id_rank:
                    print("%i sends wavefront" % rank)
                    comm.send(my_wavefront, dest=0, tag=11)
            comm.barrier()

        if rank == 0:
            addWavefrontIntensity(my_wavefront, energy, intensities)

    comm.barrier()
    return intensities


def calcualteIntensitiesAroundFirstHarmonic(undulator, number_deviation_points):

    energy = 6.04
    electron_beam = ElectronBeam(energy,0.0, 0.200, 1)

    resonance_energy = int(undulator.resonanceEnergy(electron_beam.gamma(), 0, 0))
    energies = [resonance_energy]


    #electron_beam2 = ZeroEmittanceElectronBeam(NormalDistribution(mean=energy, sigma = 0.001 * energy, norm=1.0),
    #                                           0.200)

    #electron_beam2 = ZeroEmittanceElectronBeam(DeltaDistribution(energy),
    #                                           0.200)


    #transverse_x_distribution = NormalDistribution(mean=0.0, sigma=0.00005,norm=1.0)
    #transverse_y_distribution = NormalDistribution(mean=0.0, sigma=0.0000001,norm=1.0)
    #electron_beam2.setTransverseXDistribution(transverse_x_distribution)
    #electron_beam2.setTransverseYDistribution(transverse_y_distribution)


    #electron_beam2.setElectrons(1)


    intensities = calcualteIntensitiesForEnergiesAndElectronBeams(undulator,
                                                                  energies,
                                                                  [electron_beam]) #,electron_beam2])

    return intensities

def calculateIntensities():
    filename="calcualation_save.dat"

    if Intensities.tryLoad(filename) and mpi.COMM_WORLD.Get_size() == 1:
        print("Previous calculation file found: %s" % filename)
        print("Recalculate? [y/n]")

        choice = input().lower()

        if choice=='y':
            calculate = True
        else:
            calculate = False
    else:
        calculate = True


    if calculate:
        intensities = calcualteIntensitiesAroundFirstHarmonic(undulator, 3)
        if mpi.COMM_WORLD.Get_rank() == 0:
            intensities.save(filename)
    else:
        intensities = Intensities.load(filename)

    return intensities


undulator = UndulatorVertical(1.68,
                              0.018,
                              int(4.0/0.018),
                              )

undulator2 = UndulatorVertical(1.87,
                            0.035,
                            14,
                            )

intensities = calculateIntensities()

if mpi.COMM_WORLD.Get_size() == 1:
    for energy in intensities.energies():
        #if mpi.COMM_WORLD.Get_size() > 1:
        #    intensities.approximate(energy)

        if mpi.COMM_WORLD.Get_rank() == 0:
            intensities.plotXYCuts(energy)
            intensities.plotPlane(energy)
