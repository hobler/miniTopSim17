#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Alexander Zimmel
"""

import os, sys

filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..', 'code')
sys.path.insert(0, codedir)

from miniTopSim import simulation
from surface import Surface


def test_erf():
    """
    Test if last surface of .srf file is equal to last surface of .srf_save file

    :var distance_measure:  maximum allowed difference between the two surfaces
    :var distance:          actual difference between the two surfaces
    """
    
    distance_measure = 1e-5

    simulation(os.path.join(filedir,'gauss.cfg'))
    surface1 = Surface(filename = os.path.join(filedir,'gauss.srf'))
    surface2 = Surface(filename = os.path.join(filedir,'gauss.srf_save'))

    distance = surface1.distance(surface2)
    assert distance  < distance_measure