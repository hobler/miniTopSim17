#!/usr/bin/env python3

"""
surface.py

Simulation for etching or sputtering of surfaces
@adapted: Florian Muttenthaler, 01325603 (21.11.2017)
"""

import sys
from init_surface import init_surface
import numpy as np
from math import sqrt
from statistics import mean

class Surface:
    """
    Describes the surface within the simulation

    :var self.x: numpy array of x values
    :var self.y: numpy array of y values
    """
    def __init__(self, accuracy = None, filename = None, index = None):
        '''
        3 optional parameters
        accuracy: for using the defined DELTA_X accuracy of the cfg files
        filename: for loading a surface of a srf file
        index: index of the to load surface. If None the last surface is used
        '''
        if filename!= None:
            try: 
                file = open(filename)
            except:
                print("File " + filename + " not found\nPress Enter to continue...")
                input()            
                sys.exit()
            linenum = 0
            lastlinenum = 0
            counter = 0
            for line in file:
                if 'surface' in line:
                    lastlinenum = linenum
                linenum+1
                if index!= None:
                    if counter == index:
                        break
                    else:
                        counter+1
            values = (np.loadtxt(filename,comments='surface:', skiprows=lastlinenum)).astype(np.float)
            size = values.size
            self.x = values[0:size, 0]
            self.y = values[0:size, 1]
        else:
            if accuracy != None:
                self.x = np.linspace(-50, 50, 101/accuracy)
                self.y = init_surface(self.x)
            else:
                self.x = np.linspace(-50, 50, 101)
                self.y = init_surface(self.x)
        # copies for visualization
        self.y_start = np.copy(self.y)
        self.x_start = np.copy(self.x)
                
    def distance(self, other):
        """
        calculating the distance between the self surface and an other surface
        the distance is the mean of the points from one surface to the other surface
        the distance of one point is the minimum of the distances to all other segments of the other surface
        this minimum distance is the "normal distance" or the distance at an edge of a segment
        """
        distances = []
        distances2 = []
        mindistances = []
        for x1, y1 in zip(self.x, self.y):    
            for x2, y2 in zip(other.x, other.y):
                distance = abs(sqrt((x2-x1)**2 + (y2-y1)**2))
                distances.append(distance)
            #the 2 minimumdistances ar a referenc to the points, which are neccesary to get the nearest segment
            mindistance1 = min(distances)
            for i in distances:
                if i != mindistance1:
                    distances2.append(i)
            mindistance2 = min(distances2)
            index1=distances.index(mindistance1)
            index2=distances.index(mindistance2)
            #calculation of the segment vector parameter
            segment_vecotr_x = other.x[index2]-other.x[index1]
            segment_vecotr_y = other.y[index2]-other.y[index1]
            #getting a normal vector on the segment vector            
            ny = segment_vecotr_y
            nx = -segment_vecotr_x
            #normalize the normal vector
            length = sqrt(ny**2 + nx**2)
            ny_norm = ny/length
            nx_norm = nx/length
            '''
            for checking, if segment and the normalized straight line through 
                the point of the surface are crossing each other, 
                the follwing equation system has been used (based on linear equations):
            x1 + nx_norm * t = other.x[index1] + segment_vecotr_x * r
            y1 + ny_norm * t = other.y[index1] + segment_vecotr_y * r
            ----------------------------------------------------------
            after eleminating r, t has been calculated
            Condition for crossing: 0 <= t <= 1
            '''
            if nx_norm != 0:
                t_numerator = y1 - other.y[index1] + ny_norm/nx_norm*(other.x[index1] - x1)
                t_denominator = segment_vecotr_y - ny_norm/nx_norm*segment_vecotr_x
                if t_denominator != 0:
                    t = t_numerator/t_denominator
                    if 0 <= t <= 1:
                        '''
                        the distance along the normal vector is
                        the in product of the normal vector and
                        the vector between the point on the surface on the nearer on the segment
                        '''
                        mindistance = abs(nx_norm*(other.x[index1] - x1) + ny_norm*(other.y[index1] - y1))
                    else:
                        mindistance = mindistance1
                else:
                    mindistance = mindistance1
            else:
                mindistance = mindistance1
            distances.clear()
            distances2.clear()
            mindistances.append(mindistance)
        return mean(mindistances)

    def normal(self):
        """
        Calculates the normalized vector along the surface

        :return: tuple of normalized x and y values
        """
        # extend arrays for subtraction
        x = np.zeros(self.x.size + 2)
        y = np.zeros(self.y.size + 2)
        x[1:-1] = self.x
        y[1:-1] = self.y
        x[0] = x[1]
        x[-1] = x[-2]
        y[0] = y[1]
        y[-1] = y[-2]

        dx = np.zeros(self.x.size)
        dy = np.zeros(self.y.size)

        dx = x[2:] - x[:-2]
        dy = y[2:] - y[:-2]
        length = np.linalg.norm([dx, dy], axis=0)
        return dy / length, -dx / length

    def write(self, filename, time):
        """
        Write header and surface x, y values for the given time

        :param filename: name of output file
        :param time: current timestep of the surface simulation
        """
        filename = '{}.srf'.format(filename)
        header = 'surface: {} {} x-positions y-positions\n'.format(time, len(self.x))
        with open(filename, 'a') as fp:
            fp.write(header)
            for x, y in zip(self.x, self.y):
                fp.write("{} {}\n".format(x, y))


if __name__ == '__main__':
    print("The file {} should be imported, not called directly.".format(sys.argv[0]))
