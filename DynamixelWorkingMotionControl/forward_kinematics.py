import ctypes
import os
import numpy as np
import time

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Length of the arms
a0 				= 10   
a1 				= 5
a2 				= 20
# Angles of the joints
t0 				= 0
t1				= 0 
t2				= 0

# Angles in radians
t0 		= t0/180*np.pi
t1 		= t1/180*np.pi
t2 		= t2/180*np.pi

# Control Table address
ADDR_TORQUE_ENABLE                 = 64
ADDR_PROFILE_VELOCITY              = 112
ADDR_PROFILE_ACCELERATION          = 108
ADDR_GOAL_POSITION                 = 116
ADDR_PRESENT_POSITION              = 132
ADDR_DRIVE_MODE                    = 10
ADDR_MOVING_STATUS                 = 123

# Data Byte Length
LEN_GOAL_POSITION       = 4
LEN_PRESENT_POSITION    = 4

# Protocol version
PROTOCOL_VERSION            = 2.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL1_ID                     = 71                 # Dynamixel#1 ID : 1
DXL2_ID                     = 72                 # Dynamixel#1 ID : 2
BAUDRATE                    = 1000000             # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/ttyUSB0'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
#DXL1_MIN_POSITION_VALUE     = -1000			# Dynamixel 1 will rotate between this value
#DXL1_MAX_POSITION_VALUE     = 1000		# and this value 
#DXL2_MIN_POSITION_VALUE     = -2000 		# Dynamixel 2 will rotate between this value
#DXL2_MAX_POSITION_VALUE     = 2000		# and this value
DXL_MOVING_STATUS_THRESHOLD = 20 		# Dynamixel moving status threshold

index = 0
dxl1_goal_position = [DXL1_MIN_POSITION_VALUE, DXL1_MAX_POSITION_VALUE]         # Goal position of dynamixel 1
dxl2_goal_position = [DXL2_MIN_POSITION_VALUE, DXL2_MAX_POSITION_VALUE]         # Goal position of dynamixel 2

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Initialize GroupBulkWrite instance
groupBulkWrite = GroupBulkWrite(portHandler, packetHandler)

# Initialize GroupBulkRead instace for Present Position
groupBulkRead = GroupBulkRead(portHandler, packetHandler)

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

# Enable Dynamixel Torque DXL1
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel 1 has been successfully connected")

# Enable Dynamixel Torque DXL2
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel 2 has been successfully connected")

# Add parameter storage for Dynamixel#1 present position
dxl_addparam_result = groupBulkRead.addParam(DXL1_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
if dxl_addparam_result != True:
    print("[ID:%03d] groupBulkRead addparam failed" % DXL1_ID)
    quit()

# Add parameter storage for Dynamixel#2 present position
dxl_addparam_result = groupBulkRead.addParam(DXL2_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
if dxl_addparam_result != True:
    print("[ID:%03d] groupBulkRead addparam failed" % DXL2_ID)
    quit()


def end_eff_pos(t0,t1,te):
    # Parameter table with columns " theta, alpha, r or a, d 
    
    param_tab = [[t0 ,      0         ,  a0   ,  0  ],
                 [t1 ,      0         ,  a1   ,  0  ],
                 [t2 ,      0         ,  a2   ,  0  ]]
    
    # Transformation matrix

    i=0
    T0_1 = [[np.cos(param_tab[i][0]) , -np.cos(param_tab[i][1])*np.sin(param_tab[i][0]), np.sin(param_tab[i][1])*np.sin(param_tab[i][0])  , param_tab[i][2]*np.cos(param_tab[i][0])],
            [np.sin(param_tab[i][0]) , np.cos(param_tab[i][1])*np.cos(param_tab[i][0]) , -np.sin(param_tab[i][1])*np.cos(param_tab[i][0]) , param_tab[i][2]*np.sin(param_tab[i][0])],
            [           0            ,            np.sin(param_tab[i][1])              ,       np.cos(param_tab[i][1])                    ,     param_tab[i][3]                    ],
            [0  ,  0  ,  0  ,  1 ]]

    i=1
    T1_2 = [[np.cos(param_tab[i][0]) , -np.cos(param_tab[i][1])*np.sin(param_tab[i][0]), np.sin(param_tab[i][1])*np.sin(param_tab[i][0])  , param_tab[i][2]*np.cos(param_tab[i][0])],
            [np.sin(param_tab[i][0]) , np.cos(param_tab[i][1])*np.cos(param_tab[i][0]) , -np.sin(param_tab[i][1])*np.cos(param_tab[i][0]) , param_tab[i][2]*np.sin(param_tab[i][0])],
            [           0            ,            np.sin(param_tab[i][1])              ,       np.cos(param_tab[i][1])                    ,     param_tab[i][3]                    ],
            [0  ,  0  ,  0  ,  1 ]]

    i=2
    T2_3 = [[np.cos(param_tab[i][0]) , -np.cos(param_tab[i][1])*np.sin(param_tab[i][0]), np.sin(param_tab[i][1])*np.sin(param_tab[i][0])  , param_tab[i][2]*np.cos(param_tab[i][0])],
            [np.sin(param_tab[i][0]) , np.cos(param_tab[i][1])*np.cos(param_tab[i][0]) , -np.sin(param_tab[i][1])*np.cos(param_tab[i][0]) , param_tab[i][2]*np.sin(param_tab[i][0])],
            [           0            ,            np.sin(param_tab[i][1])              ,       np.cos(param_tab[i][1])                    ,     param_tab[i][3]                    ],
            [0  ,  0  ,  0  ,  1 ]]
    
   
    




while 1:
    print("Press any key to continue! (or press ESC to quit!)")
    if getch() == chr(0x1b):
        break

    # Allocate goal position value into byte array
    param_goal_position_dxl1 = [DXL_LOBYTE(DXL_LOWORD(dxl1_goal_position[index])), DXL_HIBYTE(DXL_LOWORD(dxl1_goal_position[index])), DXL_LOBYTE(DXL_HIWORD(dxl1_goal_position[index])), DXL_HIBYTE(DXL_HIWORD(dxl1_goal_position[index]))]
    param_goal_position_dxl2 = [DXL_LOBYTE(DXL_LOWORD(dxl2_goal_position[index])), DXL_HIBYTE(DXL_LOWORD(dxl2_goal_position[index])), DXL_LOBYTE(DXL_HIWORD(dxl2_goal_position[index])), DXL_HIBYTE(DXL_HIWORD(dxl2_goal_position[index]))]
   
    # Add Dynamixel#1 goal position value to the Bulkwrite parameter storage
    dxl_addparam_result = groupBulkWrite.addParam(DXL1_ID, ADDR_GOAL_POSITION, LEN_GOAL_POSITION, param_goal_position_dxl1)
    if dxl_addparam_result != True:
        print("[ID:%03d] groupBulkWrite addparam failed" % DXL1_ID)
        quit()
    # Add Dynamixel#2 goal position value to the Bulkwrite parameter storage
    dxl_addparam_result = groupBulkWrite.addParam(DXL2_ID, ADDR_GOAL_POSITION, LEN_GOAL_POSITION, param_goal_position_dxl2)
    if dxl_addparam_result != True:
        print("[ID:%03d] groupBulkWrite addparam failed" % DXL2_ID)
        quit()


    # Bulkwrite goal position values for both the dynamixels
    dxl_comm_result = groupBulkWrite.txPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

    # Clear bulkwrite parameter storage
    groupBulkWrite.clearParam()


    while 1:
        # Bulkread present positions of both dynamixels
        dxl_comm_result = groupBulkRead.txRxPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

        # Check if groupbulkread data of Dynamixel#1 is available
        dxl_getdata_result = groupBulkRead.isAvailable(DXL1_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
        if dxl_getdata_result != True:
            print("[ID:%03d] groupBulkRead getdata failed" % DXL1_ID)
            quit()

        # Check if groupbulkread data of Dynamixel#2 is available
        dxl_getdata_result = groupBulkRead.isAvailable(DXL2_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
        if dxl_getdata_result != True:
            print("[ID:%03d] groupBulkRead getdata failed" % DXL2_ID)
            quit()

	# Get present position value
        dxl1_present_position = groupBulkRead.getData(DXL1_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
        dxl2_present_position = groupBulkRead.getData(DXL2_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)

	number = dxl1_present_position & 0xFFFFFFFF
        dxl1_present_position = ctypes.c_long(number).value

	number = dxl2_present_position & 0xFFFFFFFF
        dxl2_present_position = ctypes.c_long(number).value

	print("[ID:%03d] Present Position : %d \t [ID:%03d] LED Value: %d" % (DXL1_ID, dxl1_present_position, DXL2_ID, dxl2_present_position))

	if ((abs(dxl1_goal_position[index] - dxl1_present_position) > DXL_MOVING_STATUS_THRESHOLD) and (abs(dx2_goal_position[index] - dxl2_present_position) > DXL_MOVING_STATUS_THRESHOLD)):
	    break

    # Change goal position
    if index == 0:
        index = 1
    else:
        index = 0


# Clear bulkread parameter storage
groupBulkRead.clearParam()


# Disable Dynamixel Torque DXL1
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

# Disable Dynamixel Torque DXL2
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

# Close port
portHandler.closePort()

