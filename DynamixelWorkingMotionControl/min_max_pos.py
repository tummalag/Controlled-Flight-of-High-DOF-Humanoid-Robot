#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# Copyright 2017 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

# Author: Ki Jong Gil (Gilbert)

#
# *********     Clear Multi Turn Example      *********
#
#
# Available Dynamixel model on this example : All models using Protocol 2.0
# This example is designed for using a Dynamixel PRO 54-200, and an USB2DYNAMIXEL.
# To use another Dynamixel model, such as X series, see their details in E-Manual(emanual.robotis.com) and edit below variables yourself.
# Be sure that Dynamixel PRO properties are already set as %% ID : 1 / Baudnum : 1 (Baudrate : 57600)
#

from __future__ import print_function
import os
import ctypes
import time

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
DXL1_ID                     = 71                 # Dynamixel ID : 1
DXL2_ID		 	    = 72
BAUDRATE                    = 1000000             # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/ttyUSB0'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                                 # Value for enabling the torque 
TORQUE_DISABLE              = 0                                 # Value for disabling the torque 
DXL1_MIN_POSITION_VALUE     = -1024
DXL1_MAX_POSITION_VALUE     = 1024
DXL2_MIN_POSITION_VALUE     = -512
DXL2_MAX_POSITION_VALUE     = 512
DXL_MOVING_STATUS_THRESHOLD = 5                 # Dynamixel will rotate between this value 
EXT_POSITION_CONTROL_MODE   = 4               # Value for extended position control mode (operating mode)


ESC_ASCII_VALUE             = 0x1b
SPACE_ASCII_VALUE           = 0x20

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

# Set operating mode to extended position control mode for DXL1
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_OPERATING_MODE, EXT_POSITION_CONTROL_MODE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Operating mode changed to extended position control mode DXL1.")


# Set operating mode to extended position control mode for DXL2
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_OPERATING_MODE, EXT_POSITION_CONTROL_MODE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Operating mode changed to extended position control mode DXL2.")

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



while 1:
    #print("\nPress any key to continue! (or press ESC to quit!)")
    #if getch() == chr(ESC_ASCII_VALUE):
    #    break
    #print("  Press SPACE key to clear multi-turn information! (or press ESC to stop!)")

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

        #if index == 1:
        #    number = dxl_present_position & 0x00000FFF
        #    present_position = ctypes.c_long(number).value
        #else:
        #    number = dxl_present_position & 0xFFFFFFFF
        #    present_position = ctypes.c_long(number).value
	
	#b3 = dxl_present_position & 0xFF
	#b2 = (dxl_present_position >> 8) & 0xFF
	#b1 = (dxl_present_position >> 16)& 0xFF
	#b0 = dxl_present_position  >> 24
        #print(b3)
        #print(b2)
        #print(b1)
        #print(b0)
	number = dxl1_present_position & 0xFFFFFFFF
        dxl1_present_position = ctypes.c_long(number).value
	
 	number = dxl2_present_position & 0xFFFFFFFF
        dxl2_present_position = ctypes.c_long(number).value


        print("  [ID:%03d] GoalPos:%3d  PresPos:%3d  [ID:%03d] GoalPos:%3d  PresPos:%3d" %(DXL1_ID, dxl1_goal_position[index], dxl1_present_position, DXL2_ID, dxl2_goal_position[index], dxl2_present_position ))
 
        if kbhit():
            c = getch()
            if c == chr(SPACE_ASCII_VALUE):
                print("\n  Stop & Clear Multi-Turn Information! ")   
                # Write the present position to the goal position to stop moving DXL1
                dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, ADDR_GOAL_POSITION, dxl1_present_position)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % packetHandler.getRxPacketError(dxl_error))
                
		# Write the present position to the goal position to stop moving DXL2
                dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL2_ID, ADDR_GOAL_POSITION, dxl2_present_position)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % packetHandler.getRxPacketError(dxl_error))

                time.sleep(0.3)

                # Clear Multi-Turn Information DXL1
                dxl_comm_result, dxl_error = packetHandler.clearMultiTurn(portHandler, DXL1_ID)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % packetHandler.getRxPacketError(dxl_error))

		# Clear Multi-Turn Information DXL2
                dxl_comm_result, dxl_error = packetHandler.clearMultiTurn(portHandler, DXL2_ID)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % packetHandler.getRxPacketError(dxl_error))


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


                print("  Present Position of [ID:%03d] : %03d  and [ID:%03d]  :  %03d" % (DXL1_ID, dxl1_present_position, DXL2_ID, dxl2_present_position))
	        break

            elif c == chr(ESC_ASCII_VALUE):
                print("\n  Stopped!!")
                # Write the present position to the goal position to stop moving DXL1
                dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, ADDR_GOAL_POSITION, dxl1_present_position)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % packetHandler.getRxPacketError(dxl_error))
		# Write the present position to the goal position to stop moving DXL2
                dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL2_ID, ADDR_GOAL_POSITION, dxl2_present_position)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % packetHandler.getRxPacketError(dxl_error))

                break

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
