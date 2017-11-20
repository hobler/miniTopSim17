# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 21:14:54 2017

@author: Alexander Schreiner e1525684
Aufgabe 2: Textbasierte Parametereingabe
"""

import sys
import parameters as par
from parameters import InvalidParametersError


try:
    par.set_Parameters(str(sys.argv[1]))
    
except InvalidParametersError as e:
    print(e)

except FileNotFoundError as e:
    print(e)

finally:
    param_out = open(str(sys.argv[2]),'w')
    
    par_dict = {}
    
    par_dict['ETCHING'] = par.ETCHING
    par_dict['XMIN'] = par.XMIN
    par_dict['XMAX'] = par.XMAX
    par_dict['DELTA_X'] = par.DELTA_X
    par_dict['INITIAL_SURFACE_TYPE'] = par.INITIAL_SURFACE_TYPE
    par_dict['FUN_XMIN'] = par.FUN_XMIN
    par_dict['FUN_XMAX'] = par.FUN_XMAX
    par_dict['TIME_STEP'] = par.TIME_STEP
    par_dict['TOTAL_TIME'] = par.TOTAL_TIME
    par_dict['ETCH_RATE'] = par.ETCH_RATE
    par_dict['PLOT_SURFACE'] = par.PLOT_SURFACE
    
    param_out.write(str(par_dict))
    
    param_out.close()
    
    

    
