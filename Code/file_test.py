
# This is a simple example of a Spike Custom System Programming Language program. Without ai.
import force_sensor, distance_sensor, motor, motor_pair
from hub import port
import time
from app import linegraph as ln
import runloop
from math import *
import random
import math

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
async def module(degrees=0, speed=1110, acceleration=10000):
    if (degrees > 0):
        await motor.run_for_degrees(motor_module, degrees, speed, acceleration=acceleration)
    elif (degrees < 0):
        await motor.run_for_degrees(motor_module, degrees, speed, acceleration=acceleration)
    elif (degrees == 0):
        print('Error')
async def drive(distance=0, multiplier=14, speed=1000, acceleration=1000):
    if (distance > 0):
        degrees = (distance * calibration)
        await motor_pair.move_for_degrees(pair, degrees, 0, velocity=speed, acceleration=acceleration)
    elif (distance < 0):
        degrees = distance * calibration
        await motor_pair.move_for_degrees(pair, degrees, 0, velocity=speed, acceleration=acceleration)
    elif (distance == 0):
        print('Null Value Error')
async def tank(degrees=0, left_speed=1000, right_speed=1000, acceleration=1000):
    #180 degrees = 90 Grad
    if (degrees > 0):
        await motor_pair.move_tank_for_degrees(pair, -degrees, left_speed, -right_speed, acceleration=acceleration)
    elif (degrees < 0):
        await motor_pair.move_tank_for_degrees(pair, degrees, -left_speed, right_speed, acceleration=acceleration)
    elif (degrees == 0):
        print('Null Value Error')
async def obstacle(distance=0, speed=1000, acceleration=1000):
    if (distance > 0):
        while distance_sensor.distance(port.C) > distance:
            await drive(2, 14, speed, acceleration)
        print('Obstacle detected!')
    elif (distance <= 0):
        print('Null Value Error')
async def switch(switch=False):
    while switch == False:
        if (force_sensor.force(force_module) >= 50):
            switch = True
            return True
async def calibrate(speed=1000, acceleration=1000):
    if (distance_sensor.distance(port.C) < 110):
        print('Calibration not possible! | Distance to small!')
    elif (distance_sensor.distance(port.C) > 110):
        try:
            await drive(-1, 14, speed, acceleration)
            distance0 = distance_sensor.distance(port.C)
            await drive(10, 14, speed, acceleration)
            distance1 = distance_sensor.distance(port.C)
            calibration = distance0 - distance1
            #print('Calibration done!')
            print(calibration)
            wait(0.5)
        except:
            print('Calibration not possible! | Error!')
data = [
    {'Calibration': 1.0, 'Akku': 100, 'Wheelusage': 1.0, 'Multiplication': 1.00},
    {'Calibration': 1.0, 'Akku': 900, 'Wheelusage': 0.9, 'Multiplication': 1.10},
    {'Calibration': 1.0, 'Akku': 800, 'Wheelusage': 0.8, 'Multiplication': 1.25},
    {'Calibration': 0.9, 'Akku': 100, 'Wheelusage': 1.0, 'Multiplication': 1.10},
    {'Calibration': 1.1, 'Akku': 100, 'Wheelusage': 1.0, 'Multiplication': 0.95}
]

def euclidean_distance(point1, point2):
    multiplication = 0.0
    for key in point1:
        if key != 'Multiplication':
            multiplication += (point1[key] - point2[key]) ** 2
    return math.sqrt(multiplication)

def knn_predict(data, new_data_point, k=3):
    multiplication = []
    for item in data:
        dist = euclidean_distance(new_data_point, item)
        multiplication.append((dist, item['Multiplication']))
    multiplication.sort(key=lambda x: x[0])
    neighbors = multiplication[:k]
    total_multiplication = sum(neighbor[1] for neighbor in neighbors)
    predicted_multiplication = total_multiplication / k
    return predicted_multiplication

print('Running main Function')
async def new_function():
  print('running the new_function')
async def main():
  if await switch():
    await calibrate()
  new_data_point = {'Calibration': calibration, 'Akku': 85, 'Wheelusage': 0.95}
  calibration = knn_predict(data, new_data_point, k=3)
  print(f'Vorhergesagte Multiplikation: {calibration}')
  await drive(10)
  await new_function()
  if await switch():
    await tank(30)
  if await switch():
    await drive(10)
runloop.run(main())