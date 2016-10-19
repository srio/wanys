import pickle
import matplotlib.pyplot as plt
import numpy
import mpi4py as mpi

from orangecontrib.wanys.drivers.srw.LSFApproximation import Approximation, plotSurface

class Intensities(object):
    def __init__(self):
       self.horizontal_plots = {}
       self.vertical_plots = {}
       self.planes = {}

    def addHorizontalCut(self,energy, coordinates, intensity):
        self.horizontal_plots[energy] = (coordinates, intensity)

    def addVerticalCut(self,energy,  coordinates, intensity):
        self.vertical_plots[energy] = (coordinates, intensity)

    def addPlane(self, energy, x_coordinates, y_coordinates, intensity_plane):
        self.planes[energy] = (x_coordinates, y_coordinates, intensity_plane)

    def energies(self):
        energies = list(self.horizontal_plots.keys())
        energies.sort()

        return energies

    def plotXYCuts(self, energy):
        # Two subplots, unpack the axes array immediately
        f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
        ax1.plot(self.horizontal_plots[energy][0],
                 self.horizontal_plots[energy][1])
        ax1.set_title('Horizontal cut')
        ax2.plot(self.vertical_plots[energy][0],
                 self.vertical_plots[energy][1])
        ax2.set_title('Vertical cut')


        plt.title("Energy %f" % energy)
        mng = plt.get_current_fig_manager()
        #mng.frame.Maximize(True)
        #mng.window.showMaximized()
        plt.show()

    def plotPlane(self,energy, show_modale = True):
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        from scipy import meshgrid, array

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        x_coordinates = self.planes[energy][0]

        y_coordinates = self.planes[energy][1]

        plane = self.planes[energy][2]


	

        import scipy.interpolate
        f_int = scipy.interpolate.RectBivariateSpline(x_coordinates,y_coordinates, plane)

        x_coordinates = numpy.linspace(min(x_coordinates), max(x_coordinates), 500)
        y_coordinates = numpy.linspace(min(y_coordinates), max(y_coordinates), 500)
        plane = f_int(x_coordinates, y_coordinates)       


        X, Y = meshgrid(x_coordinates,
                        y_coordinates)

        zs = array(plane)
        print(zs.shape)
        Z = zs.reshape(X.shape)

        ax.plot_surface(X, Y, Z)
        ax.contour(X, Y, Z)

        ax.set_xlabel('X in plane')
        ax.set_ylabel('Y in plane')
        ax.set_zlabel('Intensity')

        plt.show(block=show_modale)

    def approximate(self, energy):
        x_coordinates = self.planes[energy][0]

        y_coordinates = self.planes[energy][1]

        intensity_plane = self.planes[energy][2]

        f_a = Approximation(intensity_plane, y_coordinates, x_coordinates, 5)
        z = f_a.toArray(x_coordinates, y_coordinates)
        if mpi.COMM_WORLD.Get_rank() == 0:
            plotSurface(x_coordinates, y_coordinates, z)

    def save(self, filename):
        pickle.dump(self,open(filename,"wb"))

    @staticmethod
    def tryLoad(filename):
        try:
            tmp = Intensities.load(filename)

            if not isinstance(tmp,Intensities):
                return False

        except:
            return False

        return True

    @staticmethod
    def load(filename):
        return pickle.load(open(filename,"rb"))
