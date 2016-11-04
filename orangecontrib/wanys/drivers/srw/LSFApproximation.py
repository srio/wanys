import numpy as np
import itertools
import scipy.interpolate

#import mpi4py.MPI as mpi

class BasisFunction(object):
    def __init__(self, func, shift_x, shift_y):
        self._func = func
        self._shift_x = shift_x
        self._shift_y = shift_y

    def evaluate(self, x, y):
        if abs(x - self._shift_x) >= 2.0:
            return 0.0

        if abs(y - self._shift_y) >= 2.0:
            return 0.0

        return self._func(x - self._shift_x, y - self._shift_y)

class ExpBasisFunction(object):
    def __init__(self, shift_x, shift_y):
        self._shift_x = shift_x
        self._shift_y = shift_y

    def evaluate(self, x, y):
        if abs(x - self._shift_x) >= 0.0003:
            return 0.0

        if abs(y - self._shift_y) >= 0.0003:
            return 0.0

        return np.exp(-((x-self._shift_x) ** 2 + (y-self._shift_y) ** 2) / 0.00009)

class SincBasisFunction(object):
    def __init__(self, shift_x, shift_y):
        self._shift_x = shift_x
        self._shift_y = shift_y

    def evaluate(self, x, y):
        if abs(x - self._shift_x) >= 2.0:
            return 0.0

        if abs(y - self._shift_y) >= 2.0:
            return 0.0

        return np.sinc(np.sqrt(((x-self._shift_x) ** 2 + (y-self._shift_y) ** 2) / 0.5))


class Approximation(object):
    def __init__(self, data, x_coordinates, y_coordinates, n):

        self._x_coordiantes = x_coordinates
        self._y_coordiantes = y_coordinates

        x_shifts = np.linspace(min(x_coordinates),max(x_coordinates),n)
        y_shifts = np.linspace(min(y_coordinates),max(y_coordinates),n)

        basis_functions = self.createBasisFunctions(x_shifts, y_shifts)
        self._basis_functions = basis_functions

        b = Approximation.createVectorFromArray(data)

        A = self.createMatrix(x_coordinates, y_coordinates, basis_functions)



        if mpi.COMM_WORLD.Get_rank()==0:
            print("Starting qr")
            #c = mp.qr_solve(A, b)
            d = np.linalg.lstsq(np.array(A.tolist()),
                                np.array(b.tolist()))
            coefficients = d[0]
            print("Finished qr")
        else:
            coefficients = None

        mpi.COMM_WORLD.barrier()
        coefficients = mpi.COMM_WORLD.bcast(coefficients, root = 0)

        self._coefficients = coefficients

    def evaluate(self, x, y):
        res = 0.0 #mp.mpf(0.0)

        for c, b_f in zip(self._coefficients, self._basis_functions):
            res = res + c * b_f.evaluate(x, y)

        return res

    def createBasisFunctions(self, x_shifts, y_shifts):
        print("Building basis")

        basis_functions = []
        for shift_x, shift_y in itertools.product(x_shifts, y_shifts):
            #f = lambda x,y: mp.sinc(mp.sqrt(x**2+y**2)/0.5)
            #func = BasisFunction(f, shift_x, shift_y)
            func = ExpBasisFunction(shift_x,shift_y)
            basis_functions.append(func)
        return basis_functions


    def createMatrix(self, x_coordinates, y_coordinates, basis_functions):
        print("Building matrix")
        number_basis_functions = len(basis_functions)

        A = np.zeros((number_basis_functions, len(x_coordinates) * len(y_coordinates)))

        comm = mpi.COMM_WORLD
        rank = comm.Get_rank()
        mpi_size = comm.Get_size()

        for j, x in enumerate(itertools.product(x_coordinates, y_coordinates)):
            for i, b_f in enumerate(basis_functions):
                if(i%mpi_size==rank):
                    A[i, j] = b_f.evaluate(x[0], x[1])

        A = self._communicate_array(A.T)
        return A

    def _communicate_array(self,array):
        comm = mpi.COMM_WORLD

        if comm.rank==0:
            totals = np.zeros_like(array)
        else:
            totals = None


        comm.Reduce([array, mpi.DOUBLE],
                    [totals, mpi.DOUBLE],
                    op = mpi.SUM,
                    root = 0)

        return totals

    @staticmethod
    def arrayFromFunction(f, x_coordinates, y_coordinates):
        data = np.zeros((len(x_coordinates), len(y_coordinates)))

        for i_x, x in enumerate(x_coordinates):
            for i_y, y in enumerate(y_coordinates):
                data[i_x,i_y] =f(x,y)

        return Approximation.createVectorFromArray(data)

    @staticmethod
    def createVectorFromArray(array):
        print("Building vector")
        b = np.zeros( (array.shape[0] * array.shape[1], 1))

        for i_x in range(array.shape[0]):
            for i_y in range(array.shape[1]):
                b[i_x * array.shape[1] + i_y] = array[i_x,i_y]

        return b

    def toArray(self, x_coordiantes, y_coordiantes):
        print("To array start")
        z = np.zeros((len(x_coordiantes), len(y_coordiantes)))

        comm = mpi.COMM_WORLD
        rank = comm.Get_rank()
        mpi_size = comm.Get_size()

        for i_x, c_x in enumerate(x_coordiantes):
            if(i_x%mpi_size==rank):
                for i_y, c_y in enumerate(y_coordiantes):
                    z[i_x, i_y] = self.evaluate(c_x, c_y)
        z = self._communicate_array(z)

        print("To array end")
        return z

def plotSurface(x, y, z, contour_plot=True, title=None,filename=None):
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    from scipy import meshgrid, array

    ticks = [-200, -200, -100, 0, 100, 200]

#    plt.locator_params(axis = 'x', nbins = 7)
#    plt.locator_params(axis = 'y', nbins = 7)
#    plt.gca().set_xticklabels(ticks)
#    plt.gca().set_yticklabels(ticks)

    #plt.imshow(np.abs(z).transpose(), interpolation="gaussian",aspect='auto',extent=[-50,50,-50,50])
    #plt.title(title)
    #plt.savefig(filename, bbox_inches='tight')
    #return        

    fig = plt.figure()

    if contour_plot:
        ax = fig.add_subplot(111)
    else:
        ax = fig.add_subplot(111, projection='3d')

    x_coordinates = x
    y_coordinates = y

    f_int = scipy.interpolate.RectBivariateSpline(x_coordinates,y_coordinates, z)

    x_coordinates = np.linspace(min(x_coordinates), max(x_coordinates), 500)
    y_coordinates = np.linspace(min(y_coordinates), max(y_coordinates), 500)
    z = f_int(x_coordinates, y_coordinates)

    if isinstance(z,np.ndarray):
        plane = []
        for i_x in range(len(x_coordinates)):
            for i_y in range(len(y_coordinates)):
                plane.append(float(z[i_x,i_y]))
    else:
        plane = z

    X, Y = meshgrid(x_coordinates,
                    y_coordinates)

    zs = array(plane)

    print(zs.shape,z.shape)
    Z = z# zs.reshape(X.shape)

    if contour_plot:
        CS = ax.contour(X, Y, Z)
        CB = plt.colorbar(CS, shrink=0.8, extend='both')
    else:
        ax.plot_surface(X, Y, Z)

    ax.set_xlabel('X in plane')
    ax.set_ylabel('Y in plane')

    if not contour_plot:
        ax.set_zlabel('z')


    if title is not None:
        plt.title(title)

    if filename is None:
        plt.show()
    else:
        plt.savefig(filename, bbox_inches='tight')


if __name__ == "main":
    x_coordinates = np.linspace(-5.0,5.0,25)
    y_coordinates = x_coordinates

    f = lambda x, y: np.sinc(np.sqrt(x ** 2 + y ** 2))
    data = Approximation.arrayFromFunction(f, x_coordinates, y_coordinates)

    f_a = Approximation(data, x_coordinates, y_coordinates, 5)

    x = np.linspace(-5, 5, 100)
    y = x
    z = f_a.toArray(x,y)

    if mpi.COMM_WORLD.Get_rank() == 0:
        z = z #- Approximation.arrayFromFunction(f, x, y).reshape(100,100)
        plotSurface(x, y, z)
