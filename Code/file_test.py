import force_sensor, distance_sensor, motor, motor_pair
from hub import port
import time
from app import linegraph as ln
import runloop
from math import *
import random
pair = motor_pair.PAIR_1
motor_pair.pair(pair, port.F, port.B)
motor_module = port.E
motor_module1 = port.A
force_module = port.D
calibration = 1
average = 111
times = 1
times1 = 1
average_calibration = []
average_obs = []
ai_data = []

def write_ai_data(file):
    with open("{file}", "w") as f:
        for line in ai_data:
            f.write(line)print('initialise the Content of the file')
