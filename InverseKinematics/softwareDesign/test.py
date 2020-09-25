''' 
import fr_fk as fk

#t = (0.20314665114965644, -0.03810708184309147, -0.1511655022522028, 0.22344126640842352)

t = (0.1,0.1,0.1,0.1)
print(fk.fk('right',t)) 
'''
from time import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def increment_fun(i,j):
	return (i+0.1 , j+0.2) 




fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(0, 100), ylim=(0, 100))
ax.grid()

line, = ax.plot(x, y, 'o-', lw=2)

def init():
    """initialize animation"""
    line.set_data(x ,y)
    return line,


    

