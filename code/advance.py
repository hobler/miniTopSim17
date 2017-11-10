#!/bin/env python3

import sys


def advance(surface, dtime):
    x_normals, y_normals = surface.normal()
    surface.x += dtime * x_normals
    surface.y += dtime * y_normals


def timestep(dtime, time, end_time):
    if time + dtime <= end_time:
        return dtime
    return end_time - (time + dtime)

if __name__ == '__main__':
    print("The file {} should be imported, not called directly.".format(sys.argv[0]))