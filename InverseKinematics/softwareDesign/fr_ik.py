###
#
###

import fr_fk as fk
import right_arm as rt
import numpy as np

from numpy.linalg import pinv
from time import time
#import plotting as p
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def getDist(pos_cur, pos_des):
	#	
	d = np.array(pos_cur) - np.array(pos_des)
	c = np.sqrt(d[0]*d[0] + d[1]*d[1] + d[2]*d[2])
	return c

def getde(e_cur, e_des, el_max):
	e = tuple(np.array(e_des[1:3]) - np.array(e_cur[1:3]))
	s = np.sign(e)
	s = tuple(s * el_max)
	return s

def add_dt(x,y):
	return tuple(np.array(x) + np.array(y))

t = (0,0,0,0)
er = fk.fk('right',t)
el = fk.fk('left',t)

e_des = (0, -0.04127370851174543,-0.1709845251223143)
#e_des = (0, -0.07127370851174543,-0.2709845251223143)

err = 10.0

# set up figure and animation
fig = plt.figure()
ax = fig.add_subplot(111, xlim=(-0.5, 0.5), ylim=(-0.5, 0.5), aspect='equal', autoscale_on=False,)
ax.grid()
line, = ax.plot([], [], 'o-', lw=2)

def init():
	line.set_data([],[])
	return line,

def position():
	global t
	y,z = rt.positional_array(t)
	print(y,z)
	return (y,z)

def animate(i):
    """perform animation step"""
    line.set_data(*position())
    #time_text.set_text('time = %.1f' % pendulum.time_elapsed)
    #energy_text.set_text('energy = %.3f J' % pendulum.energy())
    return line

animate(0)

while(err > 0.01):
	dt = 0.001

	dt0 = (dt,0,0,0)
	dt1 = (0,dt,0,0)
	dt2 = (0,0,dt,0)
	dt3 = (0,0,0,dt)

	t0 = add_dt(t,dt0)
	t1 = add_dt(t,dt1)
	t2 = add_dt(t,dt2)
	t3 = add_dt(t,dt3)
	
	# Right arm parameters
	# Right arm e'(right e = er)
	er_t0 = fk.fk('right',t0)
	er_t1 = fk.fk('right',t1)
	er_t2 = fk.fk('right',t2)
	er_t3 = fk.fk('right',t3)

	# Right arm del_e
	del_er_t0 = tuple(np.array(er_t0) - np.array(er))
	del_er_t1 = tuple(np.array(er_t1) - np.array(er))
	del_er_t2 = tuple(np.array(er_t2) - np.array(er))
	del_er_t3 = tuple(np.array(er_t3) - np.array(er))

	# Jacobian elements for right arm
	del_er_y_dt0 = del_er_t0[1]/dt
	del_er_z_dt0 = del_er_t0[2]/dt

	del_er_y_dt1 = del_er_t1[1]/dt
	del_er_z_dt1 = del_er_t1[2]/dt

	del_er_y_dt2 = del_er_t2[1]/dt
	del_er_z_dt2 = del_er_t2[2]/dt

	del_er_y_dt3 = del_er_t3[1]/dt
	del_er_z_dt3 = del_er_t3[2]/dt

	# Right arm Jacobian
	j_r = np.matrix([[del_er_y_dt0 , del_er_y_dt1 , del_er_y_dt2 , del_er_y_dt3],
		   			 [del_er_z_dt0 , del_er_z_dt1 , del_er_z_dt2 , del_er_z_dt3]])

	# Right arm inverse Jacobian
	J_r_inv = pinv(j_r)

	# End of right arm
	
	##########################################
	
	# Left arm parameters 
	# Left arm e'
	el_t0 = fk.fk('left',dt0)
	el_t1 = fk.fk('left',dt1)
	el_t2 = fk.fk('left',dt2)
	el_t3 = fk.fk('left',dt3)

	# Left arm del_e
	del_t0 = tuple(np.array(el_t0) - np.array(el))
	del_t1 = tuple(np.array(el_t1) - np.array(el))
	del_t2 = tuple(np.array(el_t2) - np.array(el))
	del_t3 = tuple(np.array(el_t3) - np.array(el))

	# Jacobian elements for left arm
	deyldt0 = del_t0[1]/dt
	dezldt0 = del_t0[2]/dt

	deyldt1 = del_t1[1]/dt
	dezldt1 = del_t1[2]/dt

	deyldt2 = del_t2[1]/dt
	dezldt2 = del_t2[2]/dt

	deyldt3 = del_t3[1]/dt
	dezldt3 = del_t3[2]/dt

	#t_del_0 = J_r_inv * 
	# End effector and joint loction and orientation
	el_t0 = fk.fk('left',t0)
	el_t1 = fk.fk('left',t1)
	el_t2 = fk.fk('left',t2)
	el_t3 = fk.fk('left',t3)

	# 
	del_t0 = np.subtract(el,el_t0)
	del_t1 = np.subtract(el,el_t1)
	del_t2 = np.subtract(el,el_t2)
	del_t3 = np.subtract(el,el_t3)

	
	# End of left arm 
	#########################################




	# choose the interval based on dt and the time to animate one step
	'''
	t0 = time()
	animate(0)
	t1 = time()
	interval = 1000 * dt - (t1 - t0)
	'''
	
	##################################
	de = getde(er,e_des, 0.01)
	dt_new = np.array(np.dot(J_r_inv,de))
	
	dt_new = tuple(dt_new[0,:])
	t = tuple(np.array(t) + np.array(dt_new))

	pos_cur = fk.fk('right',t)
	err = getDist(pos_cur[0:3], e_des)
	
	ani = animation.FuncAnimation(fig, position, frames=300,interval=dt, blit=True, init_func=init)

	plt.show()

	if err < 0.01:
		print(pos_cur)
		print(t)
		break

	print(err)
	#return()
	

