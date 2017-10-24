import serial
import time
import logging
from pylab import *

logging.basicConfig(filename="sampleOut.txt", level=logging.DEBUG)

logging.BASIC_FORMAT


ser = serial.Serial("/dev/tty.OBDII-Port", 38400, timeout=1)
total_speed = 0
high_speed = 0
total_time = 0
cur_speed = 0
cur_gear = 0
cur_RPM = 0
high_RPM = 0
speed_ar = []
RPM_ar = []



def convert_to_decimal(hex):
    return round(float(int("0x" + hex, 0)), 2)

def get_speed():
    ser.write("01 0D \r") # 01 - show current data, 0D - Vehicle Speed
    speed_hex = ser.readline().split(" ") #convert response to array
    print speed_hex
    speed_KPH = convert_to_decimal(speed_hex[4]) #convert relevant portion of hex response to decimal
    return speed_KPH

def KPH_to_MPH(speed_KPH):
    return round(speed_KPH / 1.60934, 2) #round to 2 decimal points

def get_RPM():
    ser.write("01 0C \r") # 01 show current data, 0C - RPM
    RPM_hex = ser.readline().split(" ")
    param_1 = convert_to_decimal(RPM_hex[4])
    param_2 = convert_to_decimal(RPM_hex[5])
    return round(((param_1 * 256 + param_2) / 4), 2)


while cur_speed == 0:
    cur_speed = get_speed()

t0 = time.time()
while cur_speed != 0:
    cur_speed = get_speed()
    high_speed = max(high_speed, cur_speed)
    cur_RPM = get_RPM()
    high_RPM = max(high_RPM, cur_RPM)
    speed_ar.append(cur_speed)
    RPM_ar.append(cur_RPM)
    logging.info("Speed: %2.2f KM/H, %2.2f MP/H @ %5.2f RPM" % (cur_speed, KPH_to_MPH(cur_speed), cur_RPM))
    time.sleep(.5)

t0 = time.time() - t0
logging.info("The vehicle's high speed was : %2.2f KM/H, %2.2f MP/H" % (high_speed, KPH_to_MPH(high_speed)))
logging.info("The vehicle's high RMP was : %5.2f RPM" % (high_RPM))
logging.info("Test complete. Time elapsed: %s seconds" % t0)


