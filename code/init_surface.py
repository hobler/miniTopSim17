#!/usr/bin/env python3

import sys
import numpy as np


def init_surface(x):
    """
    Initialize the surface with a fixed cosine function

    :param x: numpy array representing the x values
    :return: The array given the
    """
    y = np.ma.masked_where(np.fabs(x) > 25, x)
    z = -50 * (1 + np.cos(2*np.pi*y/50))
    return z.filled(0.0)


if __name__ == '__main__':
    print("The file {} should be imported, not called directly.".format(sys.argv[0]))