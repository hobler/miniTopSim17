#!/usr/bin/env python3
import os, sys
filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..', 'code')
sys.path.insert(0, codedir)
from miniTopSim import simulation
from surface import Surface

def test_yamamura_redep_1():
    distance_measure = 1e-5

    simulation(os.path.join(filedir,'yamamura_redep_1.cfg'))
    surface1 = Surface(filename = os.path.join(filedir,'yamamura_redep_1.srf'))
    surface2 = Surface(filename = os.path.join(filedir,'yamamura_redep_1.srf_save'))

    distance = surface1.distance(surface2)
    assert distance  < distance_measure