import numpy as np
from scipy.interpolate import interp2d, RegularGridInterpolator, Rbf

class InterpolatePixelTarget:

    def __init__(self, ui_control):
        self.ui_control = ui_control
        self.calculate_interpolation()

    def calculate_interpolation(self):
        xs = np.array([(self.ui_control.coordenates[i][0] + self.ui_control.coordenates[i+9][0])/2 for i in range(9)])
        ys = np.array([(self.ui_control.coordenates[i][1] + self.ui_control.coordenates[i+9][1])/2 for i in range(9)])
        z1 = np.array([i[0] for i in self.ui_control.default_coordenates])
        z2 = np.array([i[1] for i in self.ui_control.default_coordenates])
        for i in range(9):
            self.ui_control.labels[i].configure(text=f"({xs[i]:.3f}, {ys[i]:.3f})")
        self.f = Rbf(xs, ys, z1, function='linear') # Interpola la coordenada x
        self.g = Rbf(xs, ys, z2, function='linear') # Interpola la coordenada y
        print(xs)
        print(ys)
        print(z1)
        print(z2)

    def interpolate_move(self, point):
        print(f"Point: {point}")
        f_res = self.f(point[0], point[1])
        g_res = self.g(point[0], point[1])
#        print(f"res-------------{(f_res[0],g_res[0])}--------------------")
        return (f_res, g_res)