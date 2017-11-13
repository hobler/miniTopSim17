#!/usr/bin/env python3

import sys


def advance(surface, dtime):
    """
    Calculates the next x and y values for the surface depending on the given
    timestep duration

    :param surface: whole surface object
    :param dtime: timestep duration
    """
    x_normals, y_normals = surface.normal()
    surface.x += dtime * x_normals
    surface.y += dtime * y_normals


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