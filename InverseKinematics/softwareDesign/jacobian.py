#!/usr/bin/env python
# coding: utf-8

# In[1]:

import fr_ik_h as fr
import numpy as np
import time
import matplotlib.pyplot as plt
from numpy import matrix
from numpy.linalg import inv


def end_pos(x0,y0,z0,t0,t1,t2,t3,l0,l1,l2,l3):
    y1 = y0 + l0*np.cos(t0)
    z1 = z0 + l0*np.sin(t0)
    x1 = x0

    y2 = y1 + l1*np.cos(t0 + t1)
    z2 = z1 + l1*np.sin(t0 + t1)
    x2 = x1

    y3 = y2 + l2*np.sin(t0 + t1 + t2)
    z3 = z2 - l2*np.cos(t0 + t1 + t2)
    x3 = x2

    ye = y3 + l3*np.sin(t0 + t1 + t2 + t3)
    ze = z3 - l3*np.cos(t0 + t1 + t2 + t3)
    xe = x3

    print("End eff position :(",xe,",",ye,",",ze,")")
    return xe,ye,ze

def end_orien(t0,t1,t2,t3):
    t1_1 = t0
    t2_1 = t1_1 + t1
    t3_1 = t2_1 + t2 - 1.5708
    te_1 = t3_1 + t3
    tex = te_1
    tey = 0
    tez = 0

    print("End eff orientation :",tex )
    return tex,tey,tez


def main():
    print("Please enter the following parameters ")
    x0,y0,z0 = [int(x) for x in input("Origin (x0,y0,z0) = ").split(',')]
    t0,t1,t2,t3 = [float(x) for x in input("thetas in rads(t0,t1,t2,t3) = ").split(',')]
    x,y,z = end_pos(x0,y0,z0,t0,t1,t2,t3,fr.l0,fr.l1,fr.l2,fr.l3)
    tx,ty,tz = end_orien(t0,t1,t2,t3)
 
 
main()

