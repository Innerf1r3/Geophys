import numpy as np

import numpy as np
import matplotlib.pyplot as plt

class GravitationalFunctions:
    def __init__(self, R0, M0, RAD_VEL):
        self.R0 = R0
        self.M0 = M0
        self.RAD_VEL = RAD_VEL
        self.MEASURES = {'THOUSAND_KILOMETER': 1e8, 'KILOMETER': 1e5, 'METER': 100, 'SGS': 1, 'MILIGAL': 1e3, 'EOTVOS': 1e9}
        self.PI = np.pi
        self.GRAV_CONST = 6.674e-8
        self.MASS = self.M0 * 1e3
        self.RADIUS = self.R0 * 1e5
        self.DENSITY = self.MASS / (4 / 3 * self.PI * np.power(self.RADIUS, 3))
        self.x_axis = np.linspace(0, 10 * self.RADIUS, 1000)
        self.indexes = np.array([0, 0.4 * self.RADIUS, 0.8 * self.RADIUS, self.RADIUS, 1.5 * self.RADIUS,
                                2 * self.RADIUS, 3 * self.RADIUS, 4 * self.RADIUS, 5 * self.RADIUS, 6 * self.RADIUS, 10 * self.RADIUS])

    
    def rescale(self, maximum):
        format = 2 - round(np.log10(maximum))
        return 10 ** format

    def density(self):
        # Calculate the density function in SGS using provided R0 and M0
        return self.M0 / (4 / 3 * self.PI * np.power(self.R0 * 1e5, 3))

    def V(self, rho):
        result = np.zeros_like(rho)
        mask = rho < self.R0 * 1e5
        result[mask] = 2 / 3 * self.PI * self.GRAV_CONST * self.density() * (3 * (self.R0 * 1e5) ** 2 - rho[mask] ** 2)
        result[~mask] = 4 / 3 * self.PI * self.GRAV_CONST * self.density() * (self.R0 * 1e5) ** 3 / rho[~mask]
        return result

    def DV(self, rho):
        result = np.zeros_like(rho)
        mask = rho < self.R0 * 1e5
        result[mask] = 4 / 3 * self.PI * self.GRAV_CONST * self.density() * rho[mask]
        result[~mask] = 4 / 3 * self.PI * self.GRAV_CONST * self.density() * (self.R0 * 1e5) ** 3 / (rho[~mask]) ** 2
        return result

    def D2V(self, rho):
        result = np.zeros_like(rho)
        mask = rho < self.R0 * 1e5
        result[mask] = -4 / 3 * self.PI * self.GRAV_CONST * self.density()
        result[~mask] = 8 / 3 * self.PI * self.GRAV_CONST * self.density() * (self.R0 * 1e5) ** 3 / rho[~mask] ** 3
        return result
