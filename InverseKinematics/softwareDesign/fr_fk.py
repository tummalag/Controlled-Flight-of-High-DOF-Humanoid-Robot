###
# 	This file generate the present position of the end effector for the given inputs.
###
import right_arm as fkr
import left_arm as fkl

def fk(arm,t):
	# This fuction checks left or right arm and calls the end effector position and orientation.
	if arm == 'left':
		x,y,z = fkl.end_pos(fkl.fr.x0,fkl.fr.y0,fkl.fr.z0,t[0],t[1],t[2],t[3],fkl.fr.l0,fkl.fr.l1,fkl.fr.l2,fkl.fr.l3)
		tx,ty,tz = fkl.end_orien(t[0],t[1],t[2],t[3])
		return (x,y,z,tx,ty,tz)

	elif arm =='right':
		x,y,z = fkr.end_pos(fkr.fr.x0,fkr.fr.y0,fkr.fr.z0,t[0],t[1],t[2],t[3],fkr.fr.l0,fkr.fr.l1,fkr.fr.l2,fkr.fr.l3)
		tx,ty,tz = fkr.end_orien(t[0],t[1],t[2],t[3])
		return (x,y,z,tx,ty,tz)

	else:
		return None

#t = (0,0,0,0)

#print(fk('right',t))
