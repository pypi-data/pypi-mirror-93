# Python library for the Red Robotics 'MX2' Raspberry Pi add on robotics boards.
# You can stack upto 4 MX2 boards together
# Simple python commands for controlling motors.
# Version 0.0.4 14/01/2021
# Author: Neil Lambeth. neil@redrobotics.co.uk @NeilRedRobotics

from __future__ import print_function  # Make print work with python 2 & 3
import time
import smbus

MX2_ADDR = (0x30,0x31,0x32,0x33)

#Setup I2C
try:
    bus = smbus.SMBus(1)
except FileNotFoundError:
    print('')
    print('')
    print('I2C not enabled!')
    print('Enable I2C in raspi-config')

print("MX2 Library v0.0.7 loaded")

# Check for connected MX2 boards
count =0
for i in range (4):

    try:
        bus.write_quick(MX2_ADDR[i])
        print("MX2 found on", hex(MX2_ADDR[i]))
    except OSError:
        count += 1

if count > 3:
    print ('No MX2 boards found!')

# Motor control functions

def M(num,speed): # 0 - 100
    """Speed = -100 to +100"""

    if (num % 2) == 0: # Select motor 0 for even motor numbers
        m_num = int(num/2)
        motor = 0x30
    else:
        m_num = int((num-1)/2) # Select motor 1 for odd motor numbers
        motor = 0x40

    if speed > 100:  # Make sure the value sent to the motor is 100 or less
        print("Out of range")
        speed = 100

    elif speed < -100:  # Make sure the value sent to the motor is 100 or less
        print("Out of range")
        speed = -100

    speed = int(speed * 2.55) # Make it full 8 bit

    if speed >= 0:  # Forwards
        print('Forwards')
        dir0 = 1

    elif speed < 0:  # Backwards
        print('Backwards')
        speed = abs(speed)  # Make positive
        dir0 = 0
        print (speed)

    try:
        print ('Motor',num,', Speed:',speed)
        bus.write_i2c_block_data(MX2_ADDR[m_num], motor, [dir0, speed])

    except OSError:
        print('MX2 Not Found On That Address!')
    except IndexError:
        print("MX2 Not Available On That Address!")



def M_8bit(num,speed): # 0 - 255
    """Speed = -255 to +255"""

    if (num % 2) == 0: # Select motor 0 for even motor numbers
        m_num = int(num/2)
        motor = 0x30
    else:
        m_num = int((num-1)/2) # Select motor 1 for odd motor numbers
        motor = 0x40

    if speed > 255:  # Make sure the value sent to the motor is 255 or less
        print("Out of range")
        speed = 255

    elif speed < -255:  # Make sure the value sent to the motor is 255 or less
        print("Out of range")
        speed = -255

    if speed >= 0:  # Forwards
        print('Forwards')
        dir0 = 1

    elif speed < 0:  # Backwards
        print('Backwards')
        speed = abs(speed)  # Make positive
        dir0 = 0
        print (speed)

    try:
        print ('Motor',num,', Speed:',speed)
        bus.write_i2c_block_data(MX2_ADDR[m_num], motor, [dir0, speed])
    except OSError:
        print('MX2 Not Found On That Address!')
    except IndexError:
        print("MX2 Not Available On That Address!")


def m(num,speed): # 0 - 1
    """Speed = -1 to +1"""

    if (num % 2) == 0: # Select motor 0 for even motor numbers
        m_num = int(num/2)
        motor = 0x30
    else:
        m_num = int((num-1)/2) # Select motor 1 for odd motor numbers
        motor = 0x40

    if speed > 1:  # Make sure the value sent to the motor is 100 or less
        print("Out of range")
        speed = 1

    elif speed < -1:  # Make sure the value sent to the motor is 100 or less
        print("Out of range")
        speed = -1

    speed = int(speed * 255) # Make it full 8 bit
    print (speed)

    if speed >= 0:  # Forwards
        print('Forwards')
        dir0 = 1

    elif speed < 0:  # Backwards
        print('Backwards')
        speed = abs(speed)  # Make positive
        dir0 = 0
        print (speed)

    try:
        print ('Motor',num,', Speed:',speed)
        bus.write_i2c_block_data(MX2_ADDR[m_num], motor, [dir0, speed])

    except OSError:
        print('MX2 Not Found On That Address!')
    except IndexError:
        print("MX2 Not Available On That Address!")




#-----------------------------------------------------
