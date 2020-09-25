import time
import serial
import os
import matplotlib.pyplot as plt
plt.switch_backend('agg')

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import termios, fcntl, sys, os
    from select import select
    fd = sys.stdin.fileno()
    old_term = termios.tcgetattr(fd)
    new_term = termios.tcgetattr(fd)

    def getch():   
        new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(fd, termios.TCSANOW, new_term)
        try:
            ch = sys.stdin.read(1)
        finally:      
            termios.tcsetattr(fd, termios.TCSADRAIN, old_term)
        return ch
        
    def kbhit():
        new_term[3] = (new_term[3] & ~(termios.ICANON | termios.ECHO))
        termios.tcsetattr(fd, termios.TCSANOW, new_term)
        try:
            dr,dw,de = select([sys.stdin], [], [], 0)
            if dr != []:
                return 1
        finally: 
            termios.tcsetattr(fd, termios.TCSADRAIN, old_term)
            sys.stdout.flush()

        return 0

plt.ion()
fig = plt.figure()

# Initializing port settings for Arduino
port = "/dev/ttyUSB1"
ser = serial.Serial(port,115200)
ser.flushInput()
theta,force,et = [],[],[]
while(1):
    if ser.inWaiting()>0:
        data = ser.readline().strip()
        endtime = time.time()
        ser.flushInput()
        t,f = data.split('\t')
        #print(theta,force)
        #print(data)
        theta.append(t)
        force.append(f)
        et.append(endtime)
        #print(theta,force)
        plt.scatter(et,theta,c='b',label='theta')
        plt.scatter(et,force,c='r',label='force')
        plt.legend(loc='upper right')
        plt.show()
        plt.pause(0.1)

        if kbhit():
            c = getch()
            if c == chr(ESC_ASCII_VALUE):
                print("STOPPED!!!!")
               	break
	
