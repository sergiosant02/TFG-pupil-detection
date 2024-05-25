import numpy as np
from scipy.interpolate import interp2d, RegularGridInterpolator, Rbf

class InterpolatePixelTarget:

    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.calculate_interpolation()

    def calculate_interpolation(self):
        xs = np.array([(self.app_controller.get_coordenates()[i][0] + self.app_controller.get_coordenates()[i+9][0])/2 for i in range(9)])
        ys = np.array([(self.app_controller.get_coordenates()[i][1] + self.app_controller.get_coordenates()[i+9][1])/2 for i in range(9)])
        z1 = np.array([i[0] for i in self.app_controller.get_default_coordenates()])
        z2 = np.array([i[1] for i in self.app_controller.get_default_coordenates()])
        for i in range(9):
            self.app_controller.format_text_in_label(i, f"({xs[i]:.3f}, {ys[i]:.3f})")
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
        return (f_res, g_res)