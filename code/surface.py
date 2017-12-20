#!/usr/bin/env python3

"""
surface.py

Simulation for etching or sputtering of surfaces
@adapted: Florian Muttenthaler, 01325603 (21.11.2017)
@adapted: Patrick Mayr, 10.12.2017
"""

import sys
import numpy as np
import parameters as par

from math import sqrt
from statistics import mean
from itertools import combinations as combinations
from init_surface import init_surface


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
        if filename != None and filename != '':
            try: 
                file = open(filename)
            except:
                print("File " + filename + " not found\nPress Enter to continue...")
                input()            
                sys.exit()

            counter = 0
            npoints = 0     # number of points from the surface
            nSurfaces = 0
            
            for line in file:
                if 'surface' in line:

                    s_line = line.split()
                    npoints = int(s_line[s_line.index('surface:') + 2])
                    nSurfaces = nSurfaces + 1

            if index != None:
                if index < nSurfaces:
                    counter = index
                else:
                    counter = nSurfaces-1
            else:
                counter = nSurfaces-1
                        
            values = (np.loadtxt(filename, \
                                 comments = 'surface:', \
                                 skiprows = counter * npoints + counter)).astype(np.float)
            
            self.x = values[0:npoints, 0]
            self.y = values[0:npoints, 1]
        else:
            if accuracy != None:
                self.x = np.linspace(par.XMIN, par.XMAX, \
                            (par.XMAX - par.XMIN) / accuracy + 1)
            else:
                self.x = np.linspace(par.XMIN, par.XMAX, \
                            (par.XMAX - par.XMIN + 1))

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

    def deloop(self):
        '''
        Removes loops in surface caused by moving this surface.
        Method proofs for each combination of segments if there is a intersection.
        Solves the equation:
            xi + (x(i+1) - xi) * t = xj + (x(j+1) - xj) * s
            yi + (y(i+1) - yi) * t = yj + (y(j+1) - yj) * s
        where i is the index of the first segment and j of the second
        After that method removes all Points of surface between the intersection
        and insert the intersection itself
        '''
        no_seg = self.x.size - 1

        # find all combinations of segments to proof
        index = np.array(list(combinations(range(0, no_seg), 2)))
        # delete all combinations where two segments in a row
        index = index[index[:, 1] - index[:, 0] != 1, :]
        no_comb = index.shape[0]

        # solve equation system:
        # I: a*t + b*s = e
        # II: c*t + d*s = f

        a = self.x[1::1] - self.x[:-1:1]
        a = a[index[:, 0]]
        b = self.x[:-1:1] - self.x[1::1]
        b = b[index[:, 1]]

        c = self.y[1::1] - self.y[:-1:1]
        c = c[index[:, 0]]
        d = self.y[:-1:1] - self.y[1::1]
        d = d[index[:, 1]]

        e = self.x[:-1:1][index[:, 1]] - self.x[:-1:1][index[:, 0]]
        f = self.y[:-1:1][index[:, 1]] - self.y[:-1:1][index[:, 0]]

        temp1 = np.dstack((a, b))
        temp2 = np.dstack((c, d))

        A = np.dstack((temp1, temp2)).reshape((no_comb, 2, 2))
        B = np.column_stack((e, f))

        # check if matrix A is singular
        results = np.empty([no_comb, 2])
        mask_regular = np.less(np.linalg.cond(A), 1e15)  # todo: find better value???


        results[mask_regular] = np.linalg.solve(A[mask_regular], B[mask_regular])
        results[np.logical_not(mask_regular)] = 1e15  # todo: find better value???

        # find all intersections of segments proof: 0 <= t < 1 and 0 <= s < 1
        mask_intersections = np.all([np.greater_equal(results[:, 0], 0),
                                     np.less(results[:, 0], 1),
                                     np.greater_equal(results[:, 1], 0),
                                     np.less(results[:, 1], 1)], 0)

        intersections = index[mask_intersections, :]
        relevant_results = results[mask_intersections, :]

        # get the intersection values to insert
        intersection_x = self.x[intersections[:, 0]] + \
                         relevant_results[:, 0] * (self.x[intersections[:, 0] + 1] - self.x[intersections[:, 0]])
        intersection_y = self.y[intersections[:, 1]] + \
                         relevant_results[:, 1] * (self.y[intersections[:, 1] + 1] - self.y[intersections[:, 1]])

        # delete all points between the intersections
        delete_index = np.array([0])
        cor_deletion = np.array([0])

        for intersection in intersections:
            delete_index = np.append(delete_index, np.arange(intersection[0] + 1, intersection[1] + 1))
            cor_deletion = np.append(cor_deletion, delete_index.shape[0] - 1)

        delete_index = delete_index[1::1]
        cor_deletion = cor_deletion[:-1:1]

        new_x = np.delete(self.x, delete_index)
        new_y = np.delete(self.y, delete_index)

        new_x = np.insert(new_x, intersections[:, 0] + 1 - cor_deletion, intersection_x)
        new_y = np.insert(new_y, intersections[:, 0] + 1 - cor_deletion, intersection_y)

        self.x = new_x
        self.y = new_y

    def viewFactor(self):
        '''
        Calculates the viewfactor nxn matrix from surface parameters.
        '''      
        x, y = np.zeros(self.x.size + 2), np.zeros(self.y.size + 2)
        x[1:-1], y[1:-1] = self.x, self.y
        x[0], y[0] = x[1], y[1]
        x[-1], y[-1] = x[-2], y[-2]

        dx, dy = np.zeros(self.x.size), np.zeros(self.y.size)
        dx, dy = x[2:] - x[:-2], y[2:] - y[:-2]
        length = np.linalg.norm([dx, dy], axis=0)
       
        dl = np.zeros_like(length)
        for i in range(length.size):
            if i>0:
                dl[1:-1] = (length[i] + length[i-1]) / 2
        dl[0] = dl[1]
        dl[-1] = dl[-2]
         
        xi = np.ones(self.x.size**2).reshape(self.x.size, 
             self.x.size)*self.x 
        yi = np.ones_like(xi)*self.y
        xj, yj = np.ones_like(xi)*self.x[:,np.newaxis], \
                 np.ones_like(xi)*self.y[:,np.newaxis]
        xij, yij = xi - xj, yi - yj
        nx, ny = self.normal()
        nxi, nyi = np.ones_like(xi)*nx, np.ones_like(xi)*ny
        nxj, nyj = np.ones_like(xi)*nx[:,np.newaxis], \
                   np.ones_like(xi)*ny[:,np.newaxis]
        
        cosalpha = (nxj * xij + nyj * yij) / (np.sqrt(nxj ** 2 + nyj ** 2) * \
                    np.sqrt(xij ** 2 + yij ** 2))
        cosbeta = (nxi * xij + nyi * yij) / (np.sqrt(nxi ** 2 + nyi ** 2) * \
                   np.sqrt(xij ** 2 + yij ** 2))
        deltal = np.ones_like(xi)*dl
        distij = np.sqrt(xij ** 2 + yij ** 2)
        
        fij = (cosalpha*cosbeta*deltal)/(2*distij)
        mask = (cosalpha > np.zeros_like(xi)) * (cosbeta > np.zeros_like(xi)) \
               * (np.ones_like(xi) - np.eye(self.x.size))
        return fij*mask

if __name__ == '__main__':
    print("The file {} should be imported, not called directly.".format(sys.argv[0]))
