# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 14:50:34 2017

@author: Florian Muttenthaler (01325603)
"""
import sys, os
filedir = os.path.dirname(__file__)#__file__ is the path of this script
codedir = os.path.join(filedir, '..', '..', 'code')
sys.path.insert(0, codedir)
import plot as pt

def plot_diff(fname1, fname2):
    pt.plot(fname1, fname2)

if __name__ == '__main__':
    try:
        filename1 = sys.argv[1]
        filename2 = sys.argv[2]
    except:
        filename1 = 'etch_dx1.srf'
        filename2 = 'etch_dx0_125.srf'
    plot_diff(filename1, filename2)