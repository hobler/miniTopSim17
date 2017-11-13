#!/usr/bin/env python3

"""
miniTopSim.py

Simulation for etching or sputtering of surfaces
"""

import sys
from init_surface import init_surface
import numpy as np
import matplotlib.pyplot as plt


class Surface:
    """
    Describes the surface within the simulation

    :var self.x: numpy array of x values
    :var self.y: numpy array of y values
    """
    def __init__(self):
        self.x = np.linspace(-50, 50, 101)
        self.y = init_surface(self.x)
        # copies for visualization
        self.y_start = np.copy(self.y)
        self.x_start = np.copy(self.x)

    def normal(self):
        """
        Calculates the normalized vector along the surface

        :return: tuple of normalized x and y values
        """
        # extend arrays for subtraction
        x = np.zeros(self.x.size + 2)
        y = np.zeros(self.y.size + 2)
        x[1:-1] = self.x
        y[1:-1] = self.y
        x[0] = x[1]
        x[-1] = x[-2]
        y[0] = y[1]
        y[-1] = y[-2]

        dx = np.zeros(self.x.size)
        dy = np.zeros(self.y.size)

        dx = x[2:] - x[:-2]
        dy = y[2:] - y[:-2]
        length = np.linalg.norm([dx, dy], axis=0)
        return dy / length, -dx / length

    def plot(self, filename):
        """
        Display or store the plot of the surface

        :param filename: name of the png file to store the surface plot
        """
        fig = plt.figure()
        filename = '{}.png'.format(filename)
        plt.plot(self.x_start, self.y_start, 'b+-', label='Start')
        plt.plot(self.x, self.y, 'r+-', label='End')
        plt.legend(loc=0)
        fig.savefig(filename, dpi=300)
        #plt.show()

    def write(self, filename, time):
        """
        Write header and surface x, y values for the given time

        :param filename: name of output file
        :param time: current timestep of the surface simulation
        """
        filename = '{}.srf'.format(filename)
        header = 'surface: {}, {}, x-positions y-positions\n'.format(time, len(self.x))
        with open(filename, 'a') as fp:
            fp.write(header)
            for x, y in zip(self.x, self.y):
                fp.write("{} {}\n".format(x, y))


if __name__ == '__main__':
    print("The file {} should be imported, not called directly.".format(sys.argv[0]))
