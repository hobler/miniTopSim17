#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Alexander Zimmel
"""
import sys, os

import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import codata

filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..', 'code')
sys.path.insert(0, codedir)

import beam


if __name__ == '__main__':
    
    f_beam_y = list()
    
    #initialize required Parameters (f_beam should have the same max. value for
    #                                 all of the three beam types)
    e = codata.value('elementary charge')
    J = 0.001
    I_gauss = 1.06*1e-12
    I_erf = 10*1e-12
    Wz = 1000
    Wx = 1000
    xc = 0
    fwhm = 100
    x_array = np.linspace(-600, 600, 1201)
    
    #calculate f_beam in the given x range
    f_beam_y.append(np.full(len(x_array), J/e))
    f_beam_y.append(beam.gauss_beam(I_gauss/e , Wz, xc, fwhm, x_array))
    f_beam_y.append(beam.erf_beam(I_erf/e, Wz, Wx, xc, fwhm, x_array))
    
    #plot the different beam types
    for item in f_beam_y:
        plt.plot(x_array, item, '-')
    
    plt.ylabel('F_beam [Atome/cm^2]')
    plt.xlabel('x [nm]')
    plt.title('Beam-Type comparison')
    plt.legend(['constant', 'gaussian', 'error function'])
    plt.show()