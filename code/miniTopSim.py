#!/usr/bin/env python3

import sys
import os
from surface import Surface
import advance
import parameters as par
from parameters import InvalidParametersError
import plot as pt

def simulation():
    """
    Main simulation function. Calculates the progress one timestep at a time
    until the end time has been reached.

    """
    surface = Surface()

    t = 0.0
    out_file = (sys.argv[1]).split('.')[0]
    #remove file if it exists. Else it will be appended with the new data.
    try:
        os.remove('{}.srf'.format(out_file))
    except OSError:
        pass

    surface.write(out_file, t)
    while t < par.TOTAL_TIME:
        # Retrieve next possible timestep
        delta = advance.timestep(par.TIME_STEP, t, par.TOTAL_TIME)
         # Update surface values
        advance.advance(surface, par.TIME_STEP)
        t += delta
        surface.write(out_file, t)
    if par.PLOT_SURFACE:
        pt.plot(os.path.abspath('{}.srf'.format(out_file)))


if __name__ == '__main__':
    try:
        in_file = sys.argv[1]
        par.set_Parameters(os.path.abspath(in_file))

        simulation()
    except IndexError:
        print("Not enough arguments. \n Usage: {} file.cfg\n".format(sys.argv[0]))
        exit(0)
    except FileNotFoundError as e:
        print(e)
        exit(0)
    except InvalidParametersError:
        exit(0)

