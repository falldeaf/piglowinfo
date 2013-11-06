#!/usr/bin/env python

##  PyGlow
##
##      python module to control Pimoronis PiGlow (http://shop.pimoroni.com/products/piglow)
##
##      for info & documentation see:    https://github.com/benleb/PYGlow
##
##  by Ben Lebherz (@ben_leb)


## import some things
import re, sys
import RPi.GPIO as rpi
from smbus import SMBus

## some addresses
I2C_ADDR = 0x54
EN_OUTPUT_ADDR = 0x00
EN_ARM1_ADDR = 0x13
EN_ARM2_ADDR = 0x14
EN_ARM3_ADDR = 0x15
UPD_PWM_ADDR = 0x16

bus = 0

class PyGlow:

    def __init__(self):

        ## check if its an old v1 or v2 raspi
        if rpi.RPI_REVISION == 1:
            i2c_bus = 0
        elif rpi.RPI_REVISION == 2:
            i2c_bus = 1
        else:
            print "Unable to determine Raspberry Pi Hardware-Revision."
            sys.exit(1)

        ## enables the leds
        self.bus = SMBus(i2c_bus)
        ## first we tell the SN3218 to enable output
        self.bus.write_byte_data(I2C_ADDR, EN_OUTPUT_ADDR, 0x01)
        ## then we ask it to enable each led arm
        self.bus.write_byte_data(I2C_ADDR, EN_ARM1_ADDR, 0xFF)
        self.bus.write_byte_data(I2C_ADDR, EN_ARM2_ADDR, 0xFF)
        self.bus.write_byte_data(I2C_ADDR, EN_ARM3_ADDR, 0xFF)


    def all(self, value):

        ## check if given brightness value is ok
        if 0 <= value <= 255:
            ## choose all leds
            leds = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
            self.set_leds(leds, value)
            self.update_leds()
        else:
            lights_off("usage: all([0-255])")


    def led(self, led, value):

        ## use set_leds & update_leds
        led = [led];
        self.set_leds(led, value)
        self.update_leds()


    def arm(self, arm, value):

        ## check if an existing arm is choosen & if brightness value is ok
        if arm == 1 and 0 <= value <= 255:
            leds = [1,2,3,4,5,6]
        elif arm == 2 and 0 <= value <= 255:
            leds = [7,8,9,10,11,12]
        elif arm == 3 and 0 <= value <= 255:
            leds = [13,14,15,16,17,18]
        else:
            self.lights_off("usage: arm([1-3],[0-255])")

        ## light up the choosen leds
        self.set_leds(leds, value)
        self.update_leds()


    def color(self, color, value):

        ## check if an available color is choosen & if brightness value is ok
        if (color == 1 or color == "white") and 0 <= value <= 255:
            leds = [6,12,18]
        elif (color == 2 or color == "blue") and 0 <= value <= 255:
            leds = [5,11,17]
        elif (color == 3 or color == "green") and 0 <= value <= 255:
            leds = [4,10,16]
        elif (color == 4 or color == "yellow") and 0 <= value <= 255:
            leds = [3,9,15]
        elif (color == 5 or color == "orange") and 0 <= value <= 255:
            leds = [2,8,14]
        elif (color == 6 or color == "red") and 0 <= value <= 255:
            leds = [1,7,13]
        else:
            self.lights_off("usage: color(<color>,[-0-255])")

        ## light up the choosen leds
        self.set_leds(leds, value)
        self.update_leds()


    def set_leds(self, leds, value):

        ## gamma correction - thanks to Jon@Pimoroni for the mapping
        gamma_table = [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,
        3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,7,7,7,7,7,7,8,8,8,8,8,8,9,9,9,9,10,10,10,10,
        10,11,11,11,11,12,12,12,13,13,13,13,14,14,14,15,15,15,16,16,16,17,17,18,18,18,19,19,20,20,20,21,21,22,22,23,23,24,24,
        25,26,26,27,27,28,29,29,30,31,31,32,33,33,34,35,36,36,37,38,39,40,41,42,42,43,44,45,46,47,48,50,51,52,53,54,55,57,58,
        59,60,62,63,64,66,67,69,70,72,74,75,77,79,80,82,84,86,88,90,91,94,96,98,100,102,104,107,109,111,114,116,119,122,124,127,
        130,133,136,139,142,145,148,151,155,158,161,165,169,172,176,180,184,188,192,196,201,205,210,214,219,224,229,234,239,244,250,255]
        ## pick the gamma-corrected value
        gc_value = gamma_table[value]

        for led in leds:
            if isinstance(led, int) and 1 <= led <= 18 and 0 <= value <= 255:
                leds = [
                    "0x00", "0x07", "0x08", "0x09", "0x06", "0x05", "0x0A", "0x12", "0x11",
                    "0x10", "0x0E", "0x0C", "0x0B", "0x01", "0x02", "0x03", "0x04", "0x0F", "0x0D"]
            elif re.match('^[a-z]+[1-3]$', str(led)) and 0 <= value <= 255:
                leds = {"red1": "0x07", "orange1": "0x08", "yellow1": "0x09", "green1": "0x06", "blue1": "0x05", "white1": "0x0A",
                        "red2": "0x12", "orange2": "0x11", "yellow2": "0x10", "green2": "0x0E", "blue2": "0x0C", "white2": "0x0B",
                        "red3": "0x01", "orange3": "0x02", "yellow3": "0x03", "green3": "0x04", "blue3": "0x0F", "white3": "0x0D"}
            else:
                self.lights_off("usage: set_leds(leds, value) | leds has to be a list of [1-18] or <color>[1-18]")

            ## write update value to the ic
            self.bus.write_byte_data(I2C_ADDR, int(leds[led], 16), gc_value)


    def update_leds(self):
    
        ## tell the ic to update the leds
        self.bus.write_byte_data(I2C_ADDR, UPD_PWM_ADDR, 0xFF)


    def lights_off(self, msg):

        ## exit function with shuts down the leds
        self.all(0)
        print msg
        sys.exit(1)
