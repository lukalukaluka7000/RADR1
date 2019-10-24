# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 11:57:11 2019

@author: lukab
"""

import numpy as np
import scipy.interpolate as si

'''
def bspline(cv, n=100, degree=3, periodic=False):
    """ Calculate n samples on a bspline

        cv :      Array ov control vertices
        n  :      Number of samples to return
        degree:   Curve degree
        periodic: True - Curve is closed
                  False - Curve is open
    """

    # If periodic, extend the point array by count+degree+1
    cv = np.asarray(cv)
    count = len(cv)

    if periodic:
        factor, fraction = divmod(count+degree+1, count)
        cv = np.concatenate((cv,) * factor + (cv[:fraction],))
        count = len(cv)
        degree = np.clip(degree,1,degree)

    # If opened, prevent degree from exceeding count-1
    else:
        degree = np.clip(degree,1,count-1)


    # Calculate knot vector
    kv = None
    if periodic:
        kv = np.arange(0-degree,count+degree+degree-1,dtype='int')
    else:
        kv = np.concatenate(([0]*degree, np.arange(count-degree+1), [count-degree]*degree))


    # Calculate query range
    u = np.linspace(periodic,(count-degree),n)


    # Calculate result
    return np.array(si.splev(u, (kv,cv.T,degree))).T
'''
def bspline(r, slozenost=100, k=3, periodic=False):

    r = np.asarray(r) #curve values
    n = len(r)

    k = np.clip(k, 1, n-1)

    Uknot = None
    
    #knot values
    Uknot = np.concatenate(([0]*k, np.arange(n-k+1), [n-k]*k)) # n-k+1, (n-k)*k
    
    #kv=np.array([0,1,2,3,4,5,6,7,8,9,10,11])
    #prvi parmatear dadne [0,0,0]
    #drugi parametar dadne array([0,1,2,3,4,5])
    #treci parametar dadne [5,5,5]
    # Calculate query range
    u = np.linspace(periodic, (n-k), slozenost)

    return np.array(si.splev(u, (Uknot, r.T, k))).T
 
tocke=[]
tocke.append([0,0,0,1])
tocke.append([0, 10, 5, 1])
tocke.append([10, 10, 10, 1])
tocke.append([10, 0, 15 ,1])
tocke.append([0, 0, 20 ,1])
tocke.append([0, 10, 25 ,1])
tocke.append([10, 10, 30 ,1])
tocke.append([10, 0, 35 ,1])
tocke.append([0, 0, 40 ,1])
tocke.append([0, 10, 45 ,1])
tocke.append([10, 10, 50 ,1])
tocke.append([10, 0, 55 ,1])
tocke = np.array(tocke)

    
arr = bspline(tocke, slozenost=100, k=3, periodic=False)


import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

mpl.rcParams['legend.fontsize'] = 10
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter(tocke[:,0], tocke[:,1], tocke[:,2], label='kontrolni poligoni')
ax.plot(tocke[:,0], tocke[:,1], tocke[:,2])
ax.scatter(arr[:,0], arr[:,1], arr[:,2], label='b_spline')
ax.legend()
plt.show()


'''
t1=[]
t2=[]
t3=[]
for i in np.arange(0,1,0.01):
    i=round(i,2)
    t1.append(cilj[i][0])
    t2.append(cilj[i][1])
    t3.append(cilj[i][2])

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter(tocke[:,0], tocke[:,1], tocke[:,2], label='kontrolni poligoni')
ax.plot(t1, t2, t3, label="trenutna b_spline")
#ax.scatter(arr[:,0], arr[:,1], arr[:,2], label='b_spline')
ax.legend()
plt.show()
'''