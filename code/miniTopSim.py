#!/usr/bin/env python3

import sys
from surface import Surface
import advance


def main(tend, dt):
    """
    Main simulation function. Calculates the progress one timestep at a time
    until the end time has been reached.

    :param tend: end time for the simulation
    :param dt: duration of the time steps
    """
    surface = Surface()

    t = 0.0
    surface.write('basic_{}_{}'.format(tend, dt), t)
    while t < tend:
        # Update surface values
        advance.advance(surface, dt)
        # Retrieve next possible timestep
        delta = advance.timestep(dt, t, tend)
        t += delta
        surface.write('basic_{}_{}'.format(tend, dt), t)
    surface.plot('basic_{}_{}'.format(tend, dt))


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Not enough arguments. \n Usage: {} endtime timesteps".format(sys.argv[0]))
        exit(0)
    main(float(sys.argv[1]), float(sys.argv[2]))
