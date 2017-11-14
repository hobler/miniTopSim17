#!/usr/bin/env python3

import sys
from surface import Surface
import advance
import parameters as par
import os
import plot as plt


def start_simulation(tend, dt, plot):
    """
    Main simulation function. Calculates the progress one timestep at a time
    until the end time has been reached.

    :param tend: end time for the simulation
    :param dt: duration of the time steps
    """
    surface = Surface()

    t = 0.0
    out_file = 'basic_{}_{}'.format(tend, dt)
    surface.write(out_file, t)
    while t < tend:
        # Update surface values
        advance.advance(surface, dt)
        # Retrieve next possible timestep
        delta = advance.timestep(dt, t, tend)
        t += delta
        surface.write(out_file, t)
    if plot:
        plt.plot(os.path.abspath('{}.srf'.format(out_file)))


if __name__ == '__main__':
    try:
        in_file = sys.argv[1]
        par.set_Parameters(os.path.abspath(in_file))

        start_simulation(float(par.TOTAL_TIME), float(par.TIME_STEP), par.PLOT_SURFACE)
    except IndexError:
        print("Not enough arguments. \n Usage: {} file.cfg\n".format(sys.argv[0]))
        exit(0)

