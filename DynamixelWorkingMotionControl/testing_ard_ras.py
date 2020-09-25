from __future__ import print_function
import os
import ctypes
import time
import serial

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

from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address
ADDR_OPERATING_MODE         = 11               # Control table address is different in Dynamixel model
ADDR_TORQUE_ENABLE          = 64               
ADDR_GOAL_POSITION          = 116
ADDR_PRESENT_POSITION       = 132

# Protocol version
PROTOCOL_VERSION            = 2.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL1_ID		                    = 91                 # Dynamixel ID : 1
DXL2_ID		 	            = 92
DXL3_ID		 	            = 93
DXL4_ID		 	            = 94
DXL5_ID		 	            = 95
DXL6_ID		 	            = 96
BAUDRATE                    = 1000000             # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/ttyUSB0'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                                 # Value for enabling the torque 
TORQUE_DISABLE              = 0                                 # Value for disabling the torque 
DXL_MOVING_STATUS_THRESHOLD = 10                 # Dynamixel will rotate between this value 

ESC_ASCII_VALUE             = 0x1b
SPACE_ASCII_VALUE           = 0x20

#index = 0
dxl1_goal_position          = 3072         # Goal position
dxl2_goal_position          = 1024         # Goal position
dxl3_goal_position          = 2048         # Goal position
dxl4_goal_position          = 2048         # Goal position
dxl5_goal_position          = 2048         # Goal position
dxl6_goal_position          = 2048         # Goal position

THETA_MAX, THETA_MIN        = 45, -45 

dxl_MIN, dxl_MAX            = 1536, 2560


# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol versionDXL1_ID
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

# Function to enable Dynamixel Torque
def enableTorque(DXL_ID):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else: print(DXL_ID,"has been successfully connected")

enableTorque(DXL1_ID)
enableTorque(DXL2_ID)
enableTorque(DXL3_ID)
enableTorque(DXL4_ID)
enableTorque(DXL5_ID)
enableTorque(DXL6_ID)

## Setting Static goal position for DXL 1,2,3,4,5,6
# Function to Write goal position 
def setGoalPosition(DXL_ID,dxl_goal_position):
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, dxl_goal_position)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

setGoalPosition(DXL1_ID,dxl1_goal_position)
setGoalPosition(DXL2_ID,dxl2_goal_position)
setGoalPosition(DXL3_ID,dxl3_goal_position)
setGoalPosition(DXL4_ID,dxl4_goal_position)
setGoalPosition(DXL5_ID,dxl5_goal_position)
setGoalPosition(DXL6_ID,dxl6_goal_position)

def getPosition(DXL_ID):
    # Read present position DXL1
    dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_POSITION)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    return dxl_present_position

dxl1_present_position = getPosition(DXL1_ID)
dxl2_present_position = getPosition(DXL2_ID)
dxl3_present_position = getPosition(DXL3_ID)
dxl4_present_position = getPosition(DXL4_ID)
dxl5_present_position = getPosition(DXL5_ID)
dxl6_present_position = getPosition(DXL6_ID)

print("  [ID:%03d] : %03d, [ID:%03d] : %03d, [ID:%03d] : %03d, [ID:%03d] : %03d, [ID:%03d] : %03d, [ID:%03d] : %03d" % (DXL1_ID, dxl1_present_position, \
    DXL2_ID, dxl2_present_position,DXL3_ID, dxl3_present_position, DXL4_ID, dxl4_present_position,DXL5_ID, dxl5_present_position, DXL6_ID, dxl6_present_position))
 
# Initializing port settings for Arduino
port = "/dev/ttyUSB1"
ser = serial.Serial(port,115200)
ser.flushInput()

print("Entering while loop")
while 1:
    with open('sysImpData.txt', mode='a') as data:
        if ser.inWaiting()>0:
            force,theta = (ser.readline().strip()).split('\t')
            ser.flushInput()
            print(theta,)

            theta,force,endtime = float(theta),float(force),time.time()
            data.write("%f, %f, %f\n" % (endtime,theta,force))
            theta = min(max(theta,THETA_MIN),THETA_MAX)         # Binding theta values in between 45 and -45 degrees 
            
            # defining the position value
            dxl5_goal_position = int((theta/90.0)*2048 + 2048)
            dxl6_goal_position = int((-theta/90.0)*2048 + 2048)
            # Binding dxl positions 
            dxl5_goal_position = min(max(dxl5_goal_position,dxl_MIN),dxl_MAX)        
            dxl6_goal_position = min(max(dxl6_goal_position,dxl_MIN),dxl_MAX)

            #print("  [ID:%03d] : %03d, [ID:%03d] : %03d" % (DXL5_ID, dxl5_goal_position, DXL5_ID, dxl6_goal_position))

            setGoalPosition(DXL5_ID,dxl5_goal_position)
            setGoalPosition(DXL6_ID,dxl6_goal_position)
            dxl5_present_position = getPosition(DXL5_ID)
            dxl5_present_position = getPosition(DXL6_ID)
            #print("  [ID:%03d] : %03d, [ID:%03d] : %03d" % (DXL5_ID, dxl5_present_position, DXL5_ID, dxl6_present_position))

            if kbhit():
                c = getch()
                if c == chr(ESC_ASCII_VALUE):
                    print("STOPPED!!!!")
                    break

# Function to Disable Dynamixel Torque DXL
def disableTorque(DXL_ID):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else: print(DXL_ID,"has been successfully disconnected")

disableTorque(DXL1_ID)
disableTorque(DXL2_ID)
disableTorque(DXL3_ID)
disableTorque(DXL4_ID)
disableTorque(DXL5_ID)
disableTorque(DXL6_ID)

# Close port
portHandler.closePort()
