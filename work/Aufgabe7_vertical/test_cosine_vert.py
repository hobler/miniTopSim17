# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 19:52:50 2017

@author: Patrick
"""

import sys, os
filedir = os.path.dirname(__file__)#__file__ is the path of this script
codedir = os.path.join(filedir, '..', '..', 'code')
sys.path.insert(0, codedir)
from miniTopSim import simulation
from surface import Surface

def test_cosine_vert():
    '''
    this test is testing the miniTopSim.py script
    the test is checking of the generate srf file has equal values to the srf_save file
    for verfing the test the methode distance() of surface.py is used
    '''
    distance_measure = 2.3
    simulation(os.path.join(filedir,'cosine_vert_1.cfg'))
    surface1 = Surface(filename = os.path.join(filedir,'cosine_vert_1.srf'))
    surface2 = Surface(filename = os.path.join(filedir,'cosine_vert_05.srf_save'))
    distance = surface1.distance(surface2)
    assert distance  < (distance_measure/2)
    