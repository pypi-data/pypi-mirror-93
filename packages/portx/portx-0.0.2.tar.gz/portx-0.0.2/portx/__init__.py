# Python library for the RedRobotics PPX (Programmable Port eXpander)
# Author: Neil Lambeth. neil@redrobotics.co.uk @NeilRedRobotics

import smbus
import time

ppx_address = (0x50,0x51,0x52,0x53)

#Setup I2C
try:
    Bus = smbus.SMBus(1)
except FileNotFoundError:
    print('')
    print('')
    print('I2C not enabled!')
    print('Enable I2C in raspi-config')

print("portx Library v0.0.2 loaded")


# Check for connected MX2 boards
count = 0
for i in range (4):

    try:
        Bus.write_quick(ppx_address[i])
        print("PPX found on", hex(ppx_address[i]))
    except OSError:
        count += 1

if count > 3:
    print ('No PPX boards found!')


# Set up some variables
speed = 0
ADR = 0

OUTPUT = 0
INPUT = 1
SERVO = 2
MOTOR = 3
ADC = 4


def motor(pin,speed):
    pin = pin + 120
    if speed >= 0:  # Forwards
        print('Forwards')
        dir = 1
        print (speed)

    elif speed < 0:  # Backwards
        print('Backwards')
        speed = abs(speed)  # Make positive
        dir = 0
        print (speed)

    try:
        Bus.write_i2c_block_data(ppx_address, pin, [dir,speed])
        pass
    except OSError:
        print('Error-------------------------------------------------------')
        pass

def gpioSet(pin,func):
    #print(pin,dir)
    pin = pin
    Bus.write_i2c_block_data(ppx_address, pin, [func])

def gpioWrite(pin,state):
    Bus.write_i2c_block_data(ppx_address, pin, [state])



# #  8bit
# def PPX_Servo(pin,pos):
#     if pos >= 0 and pos <91:
#         dir = 0
#         print('Forward')
#         print(pos)
#
#     elif pos < 0 and pos >-91:
#         dir = 1
#         pos = abs(pos)
#         print('Reverse')
#         print(pos)
#
#     Bus.write_i2c_block_data(ppx_address, SERVO, [dir, pin, pos])


# 16 bit Degrees
def servo(pin,Pos, min = 600, mid = 1500, max = 2400):

    if pin <12:
        ADR = 0
    elif pin >11 and pin <24:
        ADR = 1
        pin = pin -12
    elif pin >23 and pin <36:
        ADR = 2
        pin = pin -24
    elif pin >35 and pin <48:
        ADR = 3
        pin = pin -36
    else:
        ADR = 4

    if Pos >=0 and Pos < 91:
        S16 = (Pos/90)
        #print(S16)
        S16 = int((S16 * (max-mid)+mid))
        #print("Servo",pin,"=",S16)

        # Convert to 2x 8bit
        pos_h = S16 >> 8
        pos_l = S16 & 0xFF

        try:
            Bus.write_i2c_block_data(ppx_address[ADR], SERVO, [pin, pos_h, pos_l])
        except OSError:
            print('PPX not available with that pin number!')
        except IndexError:
            print('Pin number too high!')

    elif Pos <0 and Pos > -91:
        S16 = abs((Pos/90))
        S16 = 1 - S16
        #print(S16)
        S16 = int((S16 * (mid-min)+min))
        #print("Servo",pin,"=",S16)

        # Convert to 2x 8bit
        pos_h = S16 >> 8
        pos_l = S16 & 0xFF

        try:
            Bus.write_i2c_block_data(ppx_address[ADR], SERVO, [pin, pos_h, pos_l])
        except OSError:
            print('PPX not available with that pin number!')
        except IndexError:
            print('Pin number too high!')
    else:
        print('Out of Range!')


# 16 bit Pulse
def servo_P(pin,Pos):

    if pin <12:
        ADR = 0
    elif pin >11 and pin <24:
        ADR = 1
        pin = pin -12
    elif pin >23 and pin <36:
        ADR = 2
        pin = pin -24
    elif pin >35 and pin <48:
        ADR = 3
        pin = pin -36
    else:
        ADR = 4

    if Pos >499 and Pos <2501:
        #print ("servo",pin,"=",Pos)

        # Convert to 2x 8bit
        pos_h = Pos >> 8
        pos_l = Pos & 0xFF

        try:
            Bus.write_i2c_block_data(ppx_address[ADR], SERVO, [pin, pos_h, pos_l])
        except OSError:
            print('No servo with that pin number!')
        except IndexError:
            print('Pin number too high!')
    else:
        print('Out of Range!')


#  16 bit 0-1

def servo_1(pin,Pos, min = 800, mid = 1500, max = 2200):

    if pin <12:
        ADR = 0
    elif pin >11 and pin <24:
        ADR = 1
        pin = pin -12
    elif pin >23 and pin <36:
        ADR = 2
        pin = pin -24
    elif pin >35 and pin <48:
        ADR = 3
        pin = pin -36
    else:
        ADR = 4

    if Pos >=0 and Pos <= 1:
        Pos = int((Pos * (max-mid)+mid))
        #print("Servo",pin,"=",Pos)

        # Convert to 2x 8bit
        pos_h = Pos >> 8
        pos_l = Pos & 0xFF

        try:
            Bus.write_i2c_block_data(ppx_address[ADR], SERVO, [pin, pos_h, pos_l])
        except OSError:
            print('PPX not available with that pin number!')
        except IndexError:
            print('Pin number too high!')


    elif Pos <0 and Pos >= -1:
        Pos = abs(Pos)
        Pos = 1 - Pos
        Pos = int((Pos * (mid-min)+min))
        #print("Servo",pin,"=",Pos)

        # Convert to 2x 8bit
        pos_h = Pos >> 8
        pos_l = Pos & 0xFF

        try:
            Bus.write_i2c_block_data(ppx_address[ADR], SERVO, [pin, pos_h, pos_l])
        except OSError:
            print('PPX not available with that pin number!')
        except IndexError:
            print('Pin number too high!')
    else:
        print('Out of Range!')
