#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 21:22:49 2020

@author: sadra
"""

import numpy as np
import pypolycontain as pp

#X1=pp.zonotope( x=np.zeros((2,1)), G=np.random.normal(size=(2,3))  )
#X2=pp.zonotope( x=np.ones((2,1))*3, G=np.random.normal(size=(2,3))  )
#X1.color='red'
#X2.color='purple'
#X=pp.convex_hull(X1,X2)
#X.color='yellow'
#
#Y0=pp.ray_shooting_hyperplanes_new(X,N=3,tol=0.2)
#
#pp.visualize([X,Y0,X1,X2 ],alpha=0.3)
#
#Y1=pp.inner_optimization(X,Y0,k=0)
#Y2=pp.outer_optimization(X,Y0)
#
#Y1.color='blue'
#Y2.color='black'
#pp.visualize([X,Y0,Y1,X1,X2 ],alpha=0.5)
#pp.visualize([Y0,X,Y1 ],alpha=0.5)
#pp.visualize([Y2,Y0,X,Y1 ],alpha=0.5)

n=5
X1=pp.zonotope( x=np.zeros((n,1)), G=np.random.normal(size=(n,n))  )
X2=pp.zonotope( x=np.ones((n,1))*10*n, G=np.random.normal(size=(n,n))  )
X1.color='red'
X2.color='purple'
X=pp.convex_hull(X1,X2)
X.color='yellow'

Y0=pp.ray_shooting_hyperplanes_new(X,N=200,tol=0.2)
B=pp.bounding_box(X)
pp.visualize([B,Y0,X],alpha=0.5)
#print(pp.Hausdorff_distance(X,Y0,directed=True,k=0))
print(pp.Hausdorff_distance(X,Y0,directed=True,k=-1))
print(B.D)


#Y1=pp.inner_optimization(X,Y0,k=0)
#Y2=pp.outer_optimization(X,Y0)
