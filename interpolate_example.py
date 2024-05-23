from scipy.interpolate import LinearNDInterpolator, CloughTocher2DInterpolator, interp2d
import numpy as np
import matplotlib.pyplot as plt

x = [0.09398198127746582, -0.04704141616821289, -0.6082663536071777, 0.7337362766265869, -0.01917290687561035, -0.5813055038452148, 0.7461297512054443, 0.0946207046508789, -0.5970382690429688]
y = [1.7058486938476562, 1.6476826667785645, 1.7280430793762207, 1.5712900161743164, 1.4405927658081055, 1.5223541259765625, 1.4505877494812012, 1.6426334381103516, 1.494835376739562]
z1 = [235, 715, 1195, 235, 715, 1195,235, 715, 1195]
z2 = [195,195,195,395,395,395,595, 595, 595]


X = np.linspace(min(x), max(x))
Y = np.linspace(min(y), max(y))
X, Y = np.meshgrid(X, Y)  # 2D grid for interpolation

# Crear el interpolador para z1
interp1 = interp2d(x=x, y=y, z=z1,)

# Crear el interpolador para z2
interp2 = interp2d(x=x, y=y, z=z2)

print( f"coord: X -> {interp1(0.09398198127746582, 1.7058486938476562)}, coord: Y -> {interp2(0.09398198127746582, 1.7058486938476562)}")

"""
Z1 = interp1(X.flatten(), Y.flatten())
Z2 = interp2(X.flatten(), Y.flatten())
plt.subplot(1, 2, 1)  # Una fila, dos columnas, primera parcela
plt.pcolormesh(X, Y, Z1, shading='auto')
plt.plot(x, y, "ok", label="input point")
plt.legend()
plt.colorbar()
plt.axis("equal")

# Definir los datos para la segunda parcela
plt.subplot(1, 2, 2)  # Una fila, dos columnas, segunda parcela
plt.pcolormesh(X, Y, Z2, shading='auto')
plt.plot(x, y, "ok", label="input point")
plt.legend()
plt.colorbar()
plt.axis("equal")

plt.show()
"""