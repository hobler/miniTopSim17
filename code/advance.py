#!/usr/bin/env python3

import sys

import numpy as np

import parameters as par
import sputtering as sp
from beam import Beam
#import matplotlib.pyplot as plt #For Demo/Debug ONLY Remove before commit.

from scipy.constants import codata


def advance(surface, dtime):
    """
    Calculates the next x and y values for the surface depending on the given
    timestep duration

    :param surface: whole surface object
    :param dtime: timestep duration
    """
    vel = get_velocities(surface, dtime)

    x_normals, y_normals = surface.normal()
    
    if par.TIME_INTEGRATION == 'vertical':
        x_tmp = 0.
        y_tmp = 1 / y_normals
    else:
        x_tmp = x_normals
        y_tmp = y_normals

    surface.x += dtime * x_tmp * vel
    surface.y += dtime * y_tmp * vel
    surface.deloop()


def get_velocities(surface,dtime):
    """
    Calculates the surface velocity based on the etch rate or the surface normals and the Sputter Yield

    :param surface: whole surface object
    :return vel, the corresponding velocity for every surface point

    """

    etching=par.ETCHING
    redep=par.REDEP

    if etching:

        etch_rate = par.ETCH_RATE
        vel = np.ones_like(surface.x)
        vel*= etch_rate

    else:

        N = par.DENSITY

        #theta represents the angle between beam direction v_b [0,-1] and the normal vector v_n[nx,ny]
        #since v_b and v_n are normalized vectors, arccos(dot(v_b,v_n)) gives the angle between the two vectors,
        # with dot(v_b,v_n)=0.*nx+(-1.)*ny, theta=arccos(-ny). If the normal vector becomes positiv-> set to 0.
        nx, ny = surface.normal()
        theta = np.arccos(np.maximum(-ny,0.))

        syield=sp.sputter_yield(theta)

        F_beam = Beam() 
        F_sput=F_beam(surface.x)*syield*np.cos(theta)

        if not redep:
            #Parameters are given in cm, *1e7 to get nm/s
            vel=F_sput/N * 1e7
            
        else:
            viewfactor = surface.viewFactor()
            F_redep = np.dot(viewfactor, F_sput)
            vel = 1e7 * (F_sput - F_redep) / N

        #Check if caves emerge and adapt velocities if necessary

        x_normals, y_normals = surface.normal()
        sim_surf_x=surface.x + dtime * x_normals * vel
        sim_surf_y=surface.y + dtime * y_normals * vel

        xmax = sim_surf_x[0]
        xmin = sim_surf_x[-1]

        for it_f in range(0, sim_surf_x.size - 2):
            dy = sim_surf_y[it_f + 1] - sim_surf_y[it_f]
            if dy < 0:
                if sim_surf_x[it_f] < xmax:
                    vel[it_f] = (xmax - surface.x[it_f]) / (dtime * x_normals[it_f])

                else:
                    xmax = sim_surf_x[it_f]

        for it_b in range(sim_surf_x.size - 1, 0, -1):
            dy = sim_surf_y[it_b - 1] - sim_surf_y[it_b]
            if dy < 0:
                if sim_surf_x[it_b] > xmin:
                    vel[it_b] = (xmin - surface.x[it_b]) / (dtime * x_normals[it_b])

                else:
                    xmin = sim_surf_x[it_b]

    return vel


def timestep(dtime, time, end_time):
    """
    Calculates the next possible
    :param dtime: time step duration
    :param time: current time of simulation
    :param end_time: end time of simulation
    :return: Next timestep duration
    """
    if time + dtime <= end_time:
        return dtime
    return end_time - (time + dtime)

if __name__ == '__main__':
    print("The file {} should be imported, not called directly.".format(sys.argv[0]))