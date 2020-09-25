import matplotlib.pyplot as plt
import matplotlib.animation as animation


# set up figure and animation
fig = plt.figure()
ax = fig.add_subplot(111, xlim=(-0.5, 0.5), ylim=(-0.5, 0.5), aspect='equal', autoscale_on=False,)
ax.grid()

line = ax.plot([], [], 'o-', lw=2)
#time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

def animate(i):
    """perform animation step"""
    line.set_data(*pendulum.position())
    time_text.set_text('time = %.1f' % pendulum.time_elapsed)
    energy_text.set_text('energy = %.3f J' % pendulum.energy())
    return line, time_text, energy_text

# choose the interval based on dt and the time to animate one step
from time import time
t0 = time()
animate(0)
t1 = time()
interval = 1000 * dt - (t1 - t0)

ani = animation.FuncAnimation(fig, animate, frames=300,interval=interval, blit=True, init_func=init)\

plt.show()






'''
plt.ion()
for i in range (10,500):
    plt.plot([1,i], y, 'r', zorder=1, lw=3)
    plt.scatter([1,i], y, s=120, zorder=2)
    pylab.ylim([-5,20])
    pylab.xlim([-100,700])
    plt.draw()
    plt.pause(0.000001)
    plt.clf()

'''