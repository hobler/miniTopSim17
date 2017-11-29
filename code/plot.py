# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 15:43:47 2017

@author: Markus
@adapted: Florian Muttenthaler, 01325603 (21.11.2017)
"""

import matplotlib.pyplot as plt
import numpy as np
import sys 
 
def plot(fname, fname2 = None):  
    '''
    plotting from either one, or two srf files
    using the second file is checking by selcting fname2
    '''
    
    def read(filename):
        '''reads the file with the given name and returns a 2-dim numpy array with the x- and y- points,
           a nparray with the number of points for every surface and the number of surfaces from the file'''
      
        npoints = 0     #number of points from the surface
        surfaces = 0    #number of surfaces
        nlist = []      #list with the number of points for every surface
        
        surfaceindices = [] #floating numbers of surfaces in file
        
        try: 
            file = open(filename)
        except:
            print("File " + filename + " not found\nPress Enter to continue...")
            input()            
            sys.exit()
        
        for line in file:
            if 'surface' in line:
                    s_line = line.split()
                    npoints =int(s_line[s_line.index('surface:')+2])
                    nlist.append(npoints)
                    surfaceindex=float(s_line[s_line.index('surface:')+1])
                    surfaceindices.append(surfaceindex)

        surfaces = len(nlist)
        narray = np.array(nlist)    #numpy array with the number of points for every surface
        
        narrayindex = np.array(surfaceindices) #numpy array with the indices of all surfaecs in file
        
        
        return (np.loadtxt(filename,comments='surface:')).astype(np.float), narray, surfaces, narrayindex
    
    
    def get_values():
        '''reads and returns the xvals and yvals for the current surface'''
        
        start = 0
        for i in range(pltindex):
            start = start+narray[i]
        end = start + narray[pltindex]
        xvalues = values[start:end, 0]
        yvalues = values[start:end, 1]

        return xvalues, yvalues
    
    def get_values2():
        '''
        reads and returns the xvals and yvals for the second surface,
        which you want to plot, if have have two surface files
        the surface that is printed is the one with the closest simulation time
        in the srf file
        '''
        global indices
        global indices2
        global narray2
        global values2
        global surfaces2
        
        start = 0
        surface1index = indices[pltindex]
        for index in indices2:
            if index <= surface1index:
                surface2index = index
            else:
                if abs(index - surface1index) < (surface1index - surface2index):
                    surface2index = index
        narrayindex = indices2.tolist().index(surface2index)
        for i in range(narrayindex):
            start = start+narray2[i]
        end = start + narray2[narrayindex]
        xvalues = values2[start:end, 0]
        yvalues = values2[start:end, 1]

        return xvalues, yvalues
    
    def draw():
        '''checks the parameters for the pressed buttons and draws the plot accordingly'''
        
        xvalues, yvalues = get_values()

        if delete:
            while ax.lines:
                ax.lines[0].remove()

        if boundaries == False:
            ax.relim()
            ax.autoscale()
        else:
            ax.set_xlim(auto=False)
            ax.set_ylim(auto=False)
        
        if aspectratio == False:
            ax.set_aspect('auto')
        else:
            ax.set_aspect('equal')
            
        ax.plot(xvalues, yvalues)
        
        if fname2 != None:
            xvalues2, yvalues2 = get_values2()
            ax.plot(xvalues2, yvalues2, '--')
        
        plt.draw()
        
    
    def onbutton(event):
        '''Handles the events that happen when a button is pressed
           'Space Button' - next surface
           '[1-9]' only show every 2^n surface
           'l' show last surface
           'r' rewind to first surface
           'a' changes aspect ratio (auto or equal)
           'd' turns delete mode on or off (delete mode = show only newest surface)
           's' saves plot to 'filename'.png
           'b' changes boundary mode (fixed or auto)
           'q' quit '''

        global potenz
        global aspectratio
        global boundaries
        global delete
        global pltindex
        global surfaces
        global narray
        global values
    
      
        if event.key == 'd':
            delete = not delete
            draw()
            
        if event.key == ' ':
            pltindex = pltindex+2**potenz
            if pltindex >= surfaces:
                pltindex = 0
            draw()

        if event.key == 'l':
            pltindex = surfaces-1
            draw()
            
        if event.key == 'r':
            pltindex=0
            if delete == False:
                delete = True
                draw()
                delete = False
            else:
                draw()
            
        if event.key == 'a':
            aspectratio = not aspectratio
            draw()
    
        if event.key == 's':
            plt.savefig(fname[:fname.index('.')]+'.png')
        
        if event.key == 'b':
            boundaries = not boundaries
            draw()
        
        if event.key == 'q':
            plt.close()
        
        if event.key == '0':
            potenz = 0
        
        if event.key == '1':
            potenz = 1
            
        if event.key == '2':
            potenz = 2
            
        if event.key == '3':
            potenz = 3
            
        if event.key == '4':
            potenz = 4
            
        if event.key == '5':
            potenz = 5
            
        if event.key == '6':
            potenz = 6
            
        if event.key == '7':
            potenz = 7
        
        if event.key == '8':
            potenz = 8
            
        if event.key == '9':
            potenz = 9

    globals()['potenz'] = 0
    globals()['aspectratio'] = False
    globals()['boundaries'] = False
    globals()['delete'] = False
    globals()['pltindex'] = 0
    globals()['values'], globals()['narray'], globals()['surfaces'], globals()['indices'] = read(fname)
    
    if fname2 != None:
        globals()['values2'], globals()['narray2'], globals()['surfaces2'], globals()['indices2'] = read(fname2)
        
    fig, ax = plt.subplots()

    plt.rcParams['keymap.xscale'] = ''
    plt.rcParams['keymap.yscale'] = ''
    plt.rcParams['keymap.save'] = 'ctrl+s'  #frees the shortcuts for the needed buttons

    draw()
    fig.canvas.mpl_connect('key_press_event', onbutton)
    plt.show()
 
if __name__ == '__main__':
    try:
        filename = sys.argv[1]       
    except:
        filename = 'trench.srf'   
    plot(filename)
    
