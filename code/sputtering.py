#!/usr/bin/env python3

import numpy as np
import parameters as par
import sputtering as sp
import os
from scipy import interpolate


class Sputter_yield_Yamamura:
    """
    Class to calculate the Sputter Yield based on the Yamamura formula.
    """

    def __init__(self, y0, f, b):
        """
        Init the Sputter Yield calculation based on the Yamamura formula.

        Y=Y_0*cos(theta)^-f * exp(b*(1-1/cos(theta)))

        :param Y0
        :param f
        :param b
        """

        self.y0 = y0
        self.f = f
        self.b = b

    def __call__(self,theta):
        """
        Get the Sputter Yield based on the Yamamura formula for a given theta

        :param theta (radians)
        :return Sputter_Yield(theta)
        """

        with np.errstate(divide='ignore'):
            cos_theta=np.cos(theta)
            syield = self.y0 * cos_theta**-self.f * np.exp(self.b * (1. - 1. / cos_theta))
        return syield


class Sputter_yield_table:
    """
    Class to estimate the Sputter Yield based on a lookup table that has to be provided by the user.
    """

    def __init__(self, file):
        """
           Init the Sputter Yield Lookup based on a *.dat file.

           :param: file -> Path to a data file that holds the angles and the corresponding Sputter Yields.

           Format:
           # theta sputter_yield
           theta_0    yield_0
           ..
           theta_n   yield_n
        """

        theta = []
        s_yield = []

        try:
            file_rel=os.path.join(os.path.dirname(__file__), ".." , "tables" , file)
            with open(file_rel) as f:
                # skip first line
                next(f)

                for line in f:
                    split = line.split()
                    theta.append(float(split[0]))
                    s_yield.append(float(split[1]))

                # Create 1d interpolation object
                self.interpolate_yield = interpolate.interp1d(np.radians(theta), s_yield)
                self.interpolate_yield.fill_value=0.
                self.interpolate_yield.bounds_error=False

        except OSError as e:
            print('Error while opening file, are you sure the file ',file_rel,' exists?')
            exit()

    def __call__(self,theta):
        """
            Estimates the Sputter Yield based on a lookup table.

            Has to be called with
            :param theta (radians)
            :return Sputter_Yield(theta)
       """


        s_yield=self.interpolate_yield(theta)
        return s_yield


def init_sputtering():
    """
       Initialize the sputter yield.

       Inits Sputter_yield_Yamamura based on the Yamamura formular if the parameter SPUTTER_YIELD_FILE=''
       Inits Sputter_yield_table  based on a table lookup and 1d interpolation if the parameter SPUTTER_YIELD_FILE !=''
    """
    global get_sputter_yield
    file=par.SPUTTER_YIELD_FILE

    if file=='':

        y0 = par.SPUTTER_YIELD_0
        f =  par.SPUTTER_YIELD_F
        b =  par.SPUTTER_YIELD_B

        yamamura=Sputter_yield_Yamamura(y0,f,b)
        get_sputter_yield=yamamura

    else:
        table=Sputter_yield_table(file)
        get_sputter_yield=table


def sputter_yield(theta):
    """
    Function that returns the Sputter Yield

    :param theta: numpy array that holds the angles.
    :return:Sputter_Yield(theta).
    """
    return get_sputter_yield(theta)


if __name__ == '__main__':
    print("The file {} should be imported, not called directly.".format(sys.argv[0]))