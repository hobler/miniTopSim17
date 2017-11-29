#!/usr/bin/env python3

"""
miniTopSim.py

Simulation for etching or sputtering of surfaces
"""

import sys
from init_surface import init_surface
import numpy as np


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

    def write(self, filename, time):
        """
        Write header and surface x, y values for the given time

        :param filename: name of output file
        :param time: current timestep of the surface simulation
        """
        filename = '{}.srf'.format(filename)
        header = 'surface: {} {} x-positions y-positions\n'.format(time, len(self.x))
        with open(filename, 'a') as fp:
            fp.write(header)
            for x, y in zip(self.x, self.y):
                fp.write("{} {}\n".format(x, y))
    def deloop(self):
        """
        Solve equation:
            vecX{i} + (VecX{i+1} - VecX{i})*s =...
                vecX{j} + (VecX{j+1} - VecX{j})*t,
        which is true for intersections.
        
        t, s       ... 0 <= l < 1 | l=t,s
        Mx  | My   ... Meshgrids for (xi-xj)|(yi-yj)
        xI,J| yI,I ... Meshgrids for (z{k+1}-z{k}) | k=i,j,z=x,y respectively
        """
        #allocating variables
        Mx , My = np.meshgrid(self.x, self.y)
        Mx = -Mx + Mx.T
        My =  My - My.T
        MxST = Mx[:-1,:-1]
        MyST = My[:-1,:-1]
        x1 = self.x[1:] - self.x[:-1]
        y1 = self.y[1:] - self.y[:-1]
        xI, xJ = np.meshgrid( x1 , x1 )
        yI, yJ = np.meshgrid( y1 ,  y1 )

        
        #solving linear equation point by point
        s = np.zeros_like(xI)
        t = np.zeros_like(xI)
        
        Denum = np.ma.array((xI*yJ - yI*xJ),mask= (xI*yJ - yI*xJ == 0))
        s = (MxST*yJ-MyST*xJ) /Denum
        Denum2    = np.ma.array(xJ, mask = (xJ == 0) )
        t = (s*xI - MxST) / Denum2
        #Intersection @ conditions for s,t
        Intersection = np.where( np.logical_and(np.logical_and( s.data >= 0, s.data < 1),
                                                np.logical_and( t.data >= 0, t.data < 1)))

        #interval deleting: redundant intervalls
        Ixy = np.asarray(Intersection).T
        overlap = np.ones_like(Ixy, dtype=bool)
        for i, arr in enumerate(Ixy):
            if i < len(Ixy)-1:
                overlap[i] = not (min(Ixy[i]) >= min(Ixy[i+1])) & (max(Ixy[i]) <= max(Ixy[i+1]))
        IntervalClear = Ixy[overlap]
        intersectionRows = np.reshape(IntervalClear, (int(len(IntervalClear)/2), 2))

        #values: new points@intersection
        xnew =  np.zeros(int(len(IntervalClear)/2))
        ynew =  np.zeros(int(len(IntervalClear)/2))
        for i, row in enumerate(intersectionRows):
            #hint: row0 -> first occurence of intersection
            xnew[i] = self.x[row[0]] + x1[row[0]]*s.data.T.item(*row)
            ynew[i] = self.y[row[0]] + y1[row[0]]*s.data.T.item(*row)
        
        #deleting crossing intervals and inserting Points@intersection
        for row, insertX, insertY in zip(reversed(intersectionRows),
                                         reversed(xnew), reversed(ynew)):
            row = sorted(row)
            deleteIndex = np.arange(*row)+1
            self.x = np.delete(self.x, deleteIndex)
            self.y = np.delete(self.y, deleteIndex)
            self.x = np.insert(self.x, min(row)+1, insertX)
            self.y = np.insert(self.y, min(row)+1, insertY) 


if __name__ == '__main__':
    print("The file {} should be imported, not called directly.".format(sys.argv[0]))
