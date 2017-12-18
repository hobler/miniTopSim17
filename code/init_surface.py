#!/usr/bin/env python3

"""
init_surface.py

@adapted: Patrick Mayr, 10.12.2017
"""

import sys
import numpy as np
import parameters as par


def init_surface(x):
    """
    Initialize the surface with a function

    :param x: numpy array representing the x values
    :return: The array given the
    """
    def flat(x):
        tmp = np.ma.masked_outside(x, par.FUN_XMIN, par.FUN_XMAX)
        y = tmp * 0.0
        return y.filled(0.0)
    
    def cosine(x):
        tmp = np.ma.masked_outside(x, par.FUN_XMIN, par.FUN_XMAX)
        y = par.FUN_PEAK_TO_PEAK * (1 + np.cos(2 * np.pi * tmp / 50))
        return y.filled(0.0)
    
    def doubleCosine(x):
        tmp = np.ma.masked_outside(x, par.FUN_XMIN, par.FUN_XMAX)
        y = par.FUN_PEAK_TO_PEAK * (1 - np.cos(2 * 2 * np.pi * tmp / 50))
        return y.filled(0.0)
        
    def step(x):
        
        # Berechnung der Punkte zwischen FUN_XMIN und FUN_XMAX als lin. Fkt.
        if (par.FUN_XMAX - par.FUN_XMIN) != 0:
            # Berechnung der Steigung
            k = - par.FUN_PEAK_TO_PEAK / (par.FUN_XMAX - par.FUN_XMIN)
        else:
            # Steigung ist unendlich, daher wird der Punkt nicht beruecksichtigt
            k = 0
            
        d = par.FUN_PEAK_TO_PEAK - k * par.FUN_XMIN
		
        tmp = np.ma.masked_outside(x, par.FUN_XMIN, par.FUN_XMAX)
        y = k * tmp + d
        
        # y-Punkte werden gesetzt, die < FUN_XMIN sind
        tmp = np.ma.masked_less_equal(x, par.FUN_XMIN)
        y[tmp.mask] = par.FUN_PEAK_TO_PEAK

        return y.filled(0.0)
        
    def vShape(x):

        # Berechnung der Punkte zwischen FUN_XMIN und 0 als lin. Fkt.
        if (0 - par.FUN_XMIN) != 0:
            # Berechnung der Steigung
            k = par.FUN_PEAK_TO_PEAK / (0 - par.FUN_XMIN)
        else:
            # Steigung ist unendlich, daher wird der Punkt nicht beruecksichtigt
            k = 0
		
        tmpX = np.ma.masked_outside(x, par.FUN_XMIN, 0)
        y = k * tmpX + par.FUN_PEAK_TO_PEAK
        
        # Berechnung der Punkte zwischen 0 und FUN_XMAX als lin. Fkt.
        if (par.FUN_XMAX - 0) != 0:
            k = - par.FUN_PEAK_TO_PEAK / (par.FUN_XMAX - 0)
        else:
            k = 0
		
        tmpX = np.ma.masked_inside(x, 0, par.FUN_XMAX)
        y[tmpX.mask] = k * x[tmpX.mask] + par.FUN_PEAK_TO_PEAK
        
        return y.filled(0.0)
                
    funcdict = {
        'Flat': flat,
        'Cosine': cosine,
        'DoubleCosine': doubleCosine,
        'Step': step,
        'V-Shape': vShape,
    } 
    
    return funcdict[par.INITIAL_SURFACE_TYPE](x)


if __name__ == '__main__':
    str = "The file {} should be imported, not called directly."
    print(str.format(sys.argv[0]))
    