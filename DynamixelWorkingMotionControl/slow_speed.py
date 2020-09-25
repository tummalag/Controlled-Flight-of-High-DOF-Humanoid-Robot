import os
import ctypes
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

# Control Table address
ADDR_TORQUE_ENABLE                 = 64
ADDR_PROFILE_VELOCITY              = 112
ADDR_PROFILE_ACCELERATION          = 108
ADDR_GOAL_POSITION                 = 116
ADDR_PRESENT_POSITION              = 132
ADDR_DRIVE_MODE                    = 10
ADDR_MOVING_STATUS                 = 123

# Data Length
LEN_ACC                       	= 4
LEN_VEL                       	= 4
LEN_GOAL_POSITION		= 4
LEN_PRESENT_POSITION		= 4

# Protocol version
PROTOCOL_VERSION = 2.0

# Default setting
DXL1_ID                     = 71                 # Dynamixel ID : 1
DXL2_ID                     = 72
BAUDRATE                    = 1000000             # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/ttyUSB0'

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                  # Value for disabling the torque
DXL1_MIN_POSITION_VALUE     = -2000
DXL1_MAX_POSITION_VALUE     = 2000
DXL2_MIN_POSITION_VALUE     = -2000
DXL2_MAX_POSITION_VALUE     = 2000

DXL_MOVING_STATUS_THRESHOLD  = 20
VELOCITY1                    = 40
ACCELERATION1                = 150
VELOCITY2                    = 250
ACCELERATION2                = 10


index = 0
dxl1_goal_position = [DXL1_MIN_POSITION_VALUE, DXL1_MAX_POSITION_VALUE]         # Goal position
dxl2_goal_position = [DXL2_MIN_POSITION_VALUE, DXL2_MAX_POSITION_VALUE]         # Goal position

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
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


# Set acceleration
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, ADDR_PROFILE_ACCELERATION, ACCELERATION1)
if dxl_comm_result != COMM_SUCCESS:
    print("%s " % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s " % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel 1 has been successfully set to desired acceleration")

# Set velocity
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, ADDR_PROFILE_VELOCITY, VELOCITY1)
if dxl_comm_result != COMM_SUCCESS:
    print("%s " % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s " % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel 1 has been successfully set to desired velocity")


# Set acceleration
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL2_ID, ADDR_PROFILE_ACCELERATION, ACCELERATION2)
if dxl_comm_result != COMM_SUCCESS:
    print("%s " % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s " % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel 2 has been successfully set to desired acceleration")

# Set velocity
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL2_ID, ADDR_PROFILE_VELOCITY, VELOCITY2)
if dxl_comm_result != COMM_SUCCESS:
    print("%s " % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s " % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel 2 has been successfully set to desired velocity")



while 1:
    print("\nPress any key to continue! (or press ESC to quit!)")
    if getch() == chr(0x1b):
        break

    # Write goal position dxl1
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, ADDR_GOAL_POSITION, dxl1_goal_position[index])
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    # Write goal position dxl2
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL2_ID, ADDR_GOAL_POSITION, dxl2_goal_position[index])
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    while 1:
        # Read present position DXL1
        dxl1_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL1_ID, ADDR_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        # Read present position DXL2
        dxl2_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL2_ID, ADDR_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

	number = dxl1_present_position & 0xFFFFFFFF
        dxl1_present_position = ctypes.c_long(number).value

	number = dxl2_present_position & 0xFFFFFFFF
        dxl2_present_position = ctypes.c_long(number).value


        print("  [ID:%03d] GoalPos:%3d  PresPos:%3d  [ID:%03d] GoalPos:%3d  PresPos:%3d" %(DXL1_ID, dxl1_goal_position[index], dxl1_present_position, DXL2_ID, dxl2_goal_position[index], dxl2_present_position ))

	if (abs(dxl1_goal_position[index] - dxl1_present_position) < DXL_MOVING_STATUS_THRESHOLD) and (abs(dxl2_goal_position[index] - dxl2_present_position) < DXL_MOVING_STATUS_THRESHOLD):
            break

    time.sleep(1)

    # Change goal position
    if index == 0:
        index = 1
    else:
        index = 0

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



