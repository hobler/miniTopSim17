#!/usr/bin/env python3
"""
miniTopSim.py

@adapted: Florian Muttenthaler, 01325603 (21.11.2017)
"""

import sys
import os
from surface import Surface
import advance
import parameters as par
from parameters import InvalidParametersError
import plot as pt
#import numpy as np


def simulation(in_file):
    """
    Main simulation function. Calculates the progress one timestep at a time
    until the end time has been reached.
    """        
    par.set_Parameters(os.path.abspath(in_file))
    surface = Surface(par.DELTA_X)#set x steps to step size of cfg file
    t = 0.0
    #splitting filename at position of the last point
    out_file, cfg_type = os.path.splitext(in_file)
    # if srf file exists, it has to be remove,
    # because you have to generate a new file with other possible values
    if os.path.exists(os.path.abspath('{}.srf'.format(out_file))):
        os.remove(os.path.abspath('{}.srf'.format(out_file)))
    surface.write(out_file, t)
    while t < par.TOTAL_TIME:
        # Retrieve next possible timestep
        delta = advance.timestep(par.TIME_STEP, t, par.TOTAL_TIME)
        # Update surface values
        advance.advance(surface, par.TIME_STEP)
        t += delta
        surface.write(out_file, t)
    if par.PLOT_SURFACE:
        if os.path.exists(os.path.abspath('{}.srf_save'.format(out_file))):
            pt.plot(os.path.abspath('{}.srf'.format(out_file)),
                    os.path.abspath('{}.srf_save'.format(out_file)))
            print('Start plot with srf_save file')
        else:
            pt.plot(os.path.abspath('{}.srf'.format(out_file)))
            print('Start plot without srf_save file')

if __name__ == '__main__':
    try:
        in_file = sys.argv[1]
        simulation(in_file)
    except IndexError:
        print("Not enough arguments. \n Usage: {} file.cfg\n".format(sys.argv[0]))
        exit(0)
    except FileNotFoundError as e:
        print(e)
        exit(0)
    except InvalidParametersError:
        exit(0)