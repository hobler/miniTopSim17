# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 15:43:47 2017

@author: Markus
"""

import matplotlib.pyplot as plt
import numpy as np
import sys 
 
def plot(fname):  
    
    class Variablen:
        def __init__(self, fname):
            self.fig, self.ax = plt.subplots()
            self.potenz = 0
            self.a = False
            self.b = False
            self.d = False
            self.pltindex = 0
            self.filename = fname
            self.values, self.narray, self.surfaces = read(self.filename)
                  
    def read(filename):
        '''reads the file with the given name and returns a 2-dim numpy array with the x- and y- points,
           a nparray with the number of points for every surface and the number of surfaces from the file'''
      
        npoints = 0     #number of points from the surface
        index = 0
        surfaces = 0    #number of surfaces
        nlist = []      #list with the number of points for every surface
        i=0
        
        try: 
            file = open(filename)
        except:
            print("File " + filename + " not found\nPress Enter to continue...")
            input()            
            sys.exit()
            
        content = file.read()
        surfaces = content.count('surface: ')
        
        for i in range(surfaces):
            npoints, index = get_surface_index(content, index)
            nlist.append(npoints)
       
        narray = np.array(nlist)    #numpy array with the number of points for every surface
        
        return (np.loadtxt(filename,comments='surface:')).astype(np.float), narray, surfaces
    
    
    def get_surface_index(content, index):
        '''returns next values for time and npoints and a index afterwards from the content file '''
        
        index = content.index('surface: ', index)
        string = content[index+13:content.index(' ', index+14)] #split
        npoints = int(string)
        
        return npoints, index+14
       
    
    def get_vals():
        '''reads and returns the xvals and yvals for the current surface'''
        
        start = 0
        for i in range(x.pltindex):
            start = start+x.narray[i]
        end = start + x.narray[x.pltindex]
        xvals = x.values[start:end, 0]
        yvals = x.values[start:end, 1]
       
        return xvals, yvals
    
    
    def draw(xvals, yvals, d):
        '''checks the parameters for the pressed buttons and draws the plot accordingly'''
        
        if d:
            while x.ax.lines:
                x.ax.lines[0].remove()
                
        if x.b == False:
            x.ax.relim()
            x.ax.autoscale()
        else:
            x.ax.set_xlim(auto=False)
            x.ax.set_ylim(auto=False)
        
        if x.a == False:
            x.ax.set_aspect('auto')
        else:
            x.ax.set_aspect('equal')
            
        x.ax.plot(xvals, yvals)
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
      
        if event.key == 'd':
            x.d = not x.d
            xvals, yvals = get_vals()
            draw(xvals, yvals, x.d)
            
        if event.key == ' ':
            x.pltindex = x.pltindex+2**x.potenz
            if x.pltindex >= x.surfaces:
                x.pltindex = 0
            xvals, yvals = get_vals()
            draw(xvals, yvals, x.d)

        if event.key == 'l':
            #x.pltindex = x.pltindex-2**x.potenz
            #if x.pltindex < 0:
                #x.pltindex = 0
            x.pltindex = x.surfaces-1   
            xvals, yvals = get_vals()
            draw(xvals, yvals, x.d)
            
        if event.key == 'r':
            x.pltindex=0
            xvals, yvals = get_vals()
            draw(xvals, yvals, True)
            
        if event.key == 'a':
            x.a = not x.a
            xvals, yvals = get_vals()
            draw(xvals, yvals, x.d)
    
        if event.key == 's':
            plt.savefig(x.filename[:x.filename.index('.')]+'.png')       
        
        if event.key == 'b':
            x.b = not x.b
            xvals, yvals = get_vals()
            draw(xvals, yvals, x.d)
        
        if event.key == 'q':
            plt.close()
        
        if event.key == '0':
            x.potenz = 0
        
        if event.key == '1':
            x.potenz = 1
            
        if event.key == '2':
            x.potenz = 2
            
        if event.key == '3':
            x.potenz = 3
            
        if event.key == '4':
            x.potenz = 4
            
        if event.key == '5':
            x.potenz = 5
            
        if event.key == '6':
            x.potenz = 6
            
        if event.key == '7':
            x.potenz = 7
        
        if event.key == '8':
            x.potenz = 8
            
        if event.key == '9':
            x.potenz = 9



    plt.rcParams['keymap.xscale'] = ''
    plt.rcParams['keymap.yscale'] = ''
    plt.rcParams['keymap.save'] = 'ctrl+s'  #frees the shortcuts for the needed buttons


    x = Variablen(fname)
    xvals, yvals = get_vals()
    draw(xvals, yvals, x.d)
    x.fig.canvas.mpl_connect('key_press_event', onbutton)
    plt.show()
 
if __name__ == '__main__':
    try:
        filename = sys.argv[1]       
    except:
        filename = 'trench.srf'   
    plot(filename)
    
