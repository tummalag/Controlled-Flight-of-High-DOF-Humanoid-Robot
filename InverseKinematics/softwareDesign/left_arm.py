### 
#   This file returns the end effector position or orientation
#   When called respective fuction with necessary inputs for Left arm
###

import fr_ik_h as fr
import numpy as np

def end_pos(x0,y0,z0,t0,t1,t2,t3,l0,l1,l2,l3):
    # This fuction returns the end effector position for the given 
    # theta and lenghts of the links

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

    #print("End eff position :(",xe,",",ye,",",ze,")")
    return xe,ye,ze

def end_orien(t0,t1,t2,t3):
    # This fuction returns the end effector orientation for the given theta
    
    t1_1 = t0
    t2_1 = t1_1 + t1
    t3_1 = t2_1 + t2 - 1.5708
    te_1 = t3_1 + t3
    tex = te_1
    tey = 0
    tez = 0

    #print("End eff orientation :",tex )
    return tex,tey,tez

def positional_array(t):

    [t0,t1,t2,t3] = t

    x = np.cumsum([fr.x0,0,0,0,0])

    y = np.cumsum([fr.y0, l0*np.cos(t0), l1*np.cos(t0 + t1),   l2*np.sin(t0 + t1 + t2),   l3*np.sin(t0 + t1 + t2 + t3) ])

    z = np.cumsum([fr.z0, l0*np.sin(t0), l1*np.sin(t0 + t1), - l2*np.cos(t0 + t1 + t2), - l3*np.cos(t0 + t1 + t2 + t3) ])


def main():

    x0,y0,z0 = [int(x) for x in input("Origin (x0,y0,z0) = ").split(',')]
    t0,t1,t2,t3 = [float(x) for x in input("thetas in rads(t0,t1,t2,t3) = ").split(',')]
    x,y,z = end_pos(fr.x0,fr.y0,fr.z0,t0,t1,t2,t3,fr.l0,fr.l1,fr.l2,fr.l3)
    tx,ty,tz = end_orien(t0,t1,t2,t3)
 
 
#main()

