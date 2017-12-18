#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Alexander Zimmel
"""

import sys

import numpy as np
from scipy.special import erf
from scipy.constants import codata

import parameters as par


class Beam:
    """
    Class Beam creates an Beam-object with a type that is set by the user
    """
    
    def __init__(self, beam_type = None):
        """
        Initialize Beam-Object and set type
        
        :param beam_type:   Beam type to be used with this instance of the object
        """
        
        if beam_type == None:
            self.beam_type = par.BEAM_TYPE
        else:
            self.beam_type = beam_type
            
        self.e = codata.value('elementary charge')

        if self.beam_type == 'constant':
            self.J_e = par.BEAM_CURRENT_DENSITY / self.e
        else:    
            self.I_e = par.BEAM_CURRENT / self.e
            self.Wz = par.SCAN_WIDTH
            self.xc = par.BEAM_CENTER
            self.fwhm = par.FWHM
            if self.beam_type == 'error function': self.Wx = par.ERF_BEAM_WIDTH
    
    def __call__(self, x_array = None):  
        """
        Call method for class Beam calculates F_beam for initialized beam type
        
        :param x_array: x values used to calculate F_beam
        :return:        calculated f_beam for all x values 
        """
        
        if self.beam_type == 'constant':
            return self.J_e
        elif self.beam_type == 'Gaussian':
            return gauss_beam(self.I_e, self.Wz, self.xc, self.fwhm, x_array)
        elif self.beam_type == 'error function':
            return erf_beam(self.I_e, self.Wz, self.Wx, self.xc, self.fwhm, x_array)
        
def gauss_beam(I_e, Wz, xc, fwhm, x_array):
    """
    Calculates F_beam for a gaussian beam
    
    :param I_e:         beam current divided by elementary charge
    :param Wz:          scan width
    :param xc:          beam center
    :param fwhm:        full width at half maximum is related to the standard deviation
    :param x_array:     x values of surface
    
    :return:            calculated f_beam for all x values 
    """
        
    sigma = fwhm / np.sqrt(8*np.log(2))
    
    exp_term = np.exp((-1)*((x_array-xc)**2) / (2 * sigma**2))
    return (1e14 * exp_term * I_e / (np.sqrt(2*np.pi) * sigma * Wz))
        
        
def erf_beam(I_e, Wz, Wx, xc, fwhm, x_array):
    """
    Calculates F_beam in dependency of two error functions beam (approximated gaussian beam)
    
    :param I_e:         beam current divided by elementary charge
    :param Wz:          scan width
    :param Wx:          beam width
    :param xc:          beam center
    :param fwhm:        full width at half maximum is related to the standard deviation
    :param x_array:     x values of surface
    
    :return:            calculated f_beam for all x values 
    """
        
    sigma = fwhm / np.sqrt(8*np.log(2))

    erf_term_upper = erf((-1)*((x_array-(xc+(Wx/2)))) / (np.sqrt(2)*sigma))
    erf_term_lower = erf((-1)*((x_array-(xc-(Wx/2)))) / (np.sqrt(2)*sigma))
    erf_term = erf_term_upper - erf_term_lower
    return (1e14 * erf_term * I_e / (2 * Wx * Wz))
        

if __name__ == '__main__':
    print("The file {} should be imported, not called directly.".format(sys.argv[0]))
