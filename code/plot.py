# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 15:43:47 2017

@author: Markus
"""

import matplotlib.pyplot as plt
import numpy as np
import sys 
 
def plot(fname):  
    
    def read(filename):
        """
        reads the file with the given name and returns a 2-dim numpy array with the x- and y- points,
        a nparray with the number of points for every surface and the number of surfaces from the file
        """
      
        npoints = 0     #number of points from the surface
        surfaces = 0    #number of surfaces
        nlist = []      #list with the number of points for every surface
        
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

        surfaces = len(nlist)
        narray = np.array(nlist)    #numpy array with the number of points for every surface
        
        return (np.loadtxt(filename,comments='surface:')).astype(np.float), narray, surfaces
    
    
    def get_values():
        '''reads and returns the xvals and yvals for the current surface'''
        
        start = 0
        for i in range(pltindex):
            start = start+narray[i]
        end = start + narray[pltindex]
        xvalues = values[start:end, 0]
        yvalues = values[start:end, 1]
       
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
    globals()['values'], globals()['narray'], globals()['surfaces'] = read(fname)

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
    
