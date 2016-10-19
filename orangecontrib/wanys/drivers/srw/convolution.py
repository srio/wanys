import numpy as np

class Convolutor(object):
    def __init__(self,e_field,x_min, x_max, y_min, y_max):
        self._e_field = e_field
        self._x_min = x_min
        self._x_max = x_max
        self._y_min = y_min
        self._y_max = y_max

        self._rho = np.zeros(self._e_field_dims())
        self._buff = np.zeros(self._e_field_dims())

    def EField(self):
        return self._e_field

    def XMin(self):
        return self._x_min

    def XMax(self):
        return self._x_max

    def YMin(self):
        return self._y_min

    def YMax(self):
        return self._y_max

    def _e_field_dim_x(self):
        return self.EField().shape[0]

    def _e_field_dim_y(self):
        return self.EField().shape[1]

    def _e_field_dims(self):

        dims = (self._e_field_dim_x(),
                self._e_field_dim_y())

        return dims

    def x_coordinates(self):
        x_coordinates = np.linspace(self.XMin(), self.XMax(), self._e_field_dim_x())
        return x_coordinates

    def y_coordinates(self):
        y_coordinates = np.linspace(self.YMin(), self.YMax(), self._e_field_dim_y())
        return y_coordinates

    def weightedElectronPhaseSpaceDistribution(self, x_shift, phi_shift, a_shift):

        x_coordinates = self.x_coordinates()
        y_coordinates = self.y_coordinates()

        max_i_x = len(x_coordinates) - 1
        max_i_y = len(y_coordinates) - 1

        for i_x, x in enumerate(x_coordinates):
            for i_y, y in enumerate(y_coordinates):
                res = -( (x - x_shift[0])*(x-x_shift[0]) + (y - x_shift[1])*(y-x_shift[1]) +
                         (x - phi_shift[0])*(x-phi_shift[0]) + (y - phi_shift[1])*(y-phi_shift[1]))

                if not(i_x == 0 or i_x == max_i_x):
                    res = 2.0 * res

                if not(i_y == 0 or i_y == max_i_y):
                    res = 2.0 * res

                self._rho[i_x,i_y] = res


        self._rho = np.exp(self._rho)
        return self._rho

    def convolute(self,x_shift, phi_shift):

        x_coordinates = self.x_coordinates()
        y_coordinates = self.y_coordinates()

        res = 0.0

        max_i_x = len(x_coordinates) - 1
        max_i_y = len(y_coordinates) - 1

        for i_x, x in enumerate(x_coordinates):
            for i_y, y in enumerate(y_coordinates):
                a_shift = (x,y)
                integral_one = np.sum(self.EField() * self.weightedElectronPhaseSpaceDistribution(x_shift,phi_shift,a_shift))

                if not(i_x == 0 or i_x == max_i_x):
                    integral_one = 2.0 * integral_one

                if not(i_y == 0 or i_y == max_i_y):
                    integral_one = 2.0 * integral_one

                res = res + integral_one * self.EField()[i_x,i_y]

        return res

e_field = np.ones((100,100))

convoluter = Convolutor(e_field,-2.0,2.0,-2.0,2.0)

import time

start = time.clock()
res = convoluter.convolute((0,0),(0,0))
end = time.clock()
print("Time elapsed",end - start)
