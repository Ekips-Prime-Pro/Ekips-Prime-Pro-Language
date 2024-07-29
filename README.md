# Spike Custom Programming Language

[![Application](https://github.com/Spike-Prime-Pro/Spike-Custom-Programming-Language-and-Compiler/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/Spike-Prime-Pro/Spike-Custom-Programming-Language-and-Compiler/actions/workflows/python-app.yml)

## Introduction

Welcome to the documentation for Spike Custom System Programming! This guide will provide you with all the information you need to get started with programming in Spike Custom System Programming.
This programm is programmd to implement the Spike Prime Hub software with a easy and straight forward Programming Language that compiles in a .llsp3 file that you can put in the [Official Spike Prime Software](https://education.lego.com/de-de/downloads/spike-app/software/), this will be integratet in an future update, also the full ai functionalities will be added in v3.0

## Table of Contents

- [Installation](#installation)
- [Syntax](#syntax)
- [Functions](#functions)
- [Artificial Neural Network](#Artificial-Neural-Network)
- [Examples](#examples)
- [Full example with explaination](#full-example-with-explaination)
- [Guide](#guide)
- [Robot Recomondations](#robot-recomondations)

## Installation

To use the Spike Custom System Programming Language, you need to install the compiler and Debuger. Follow the instructions below to get started:

1. Download the latest version of the Spike Custom System Programming Language compiler from the official website or from the [github repository](https://github.com/Spike-Prime-Pro/Spike-Custom-Programming-Language-and-Compiler/releases).
2. Install the compiler on your system by running the installer.
3. Verify the installation by opening a terminal and running the programm.
4. If there is any Problem please send a Email to <Iron.ai.dev@gmail.com> for bug fixing.

## Syntax

The Spike Custom System Programming Language has a simple and intuitive syntax that is easy to read and write. Here are some key features of the syntax:

- The functions are the key part of the Programm like `sleep(10)` (`sleep`).
- The brackets define function uneque variables like `wait(1)` (`()`).
- Coments have to be after an `//` or an `#` also the content has to be enclosed in curly brackets, like that `//(you coment)`

## Functions

The main functions of the Spike Custom System Programming Language are for the basic use of the Spike Prime Custom Operating System and programming with ai enforced functions. To use the functions you have to first initialize the functions with the `init()`, `drive.init()`, `module.init()`, `ai.init()`, `calibration.init()`, `variables.init()` and `sensor.init()` functions.
There are four build in functions.

- The `drive` function is for driving a motorpair forward and backward.
- The `tank` function is for making turns.
- The `module` function is for controling a single motor.
- The `calibration` function is for calibrating the robot and it motors, it also enhances the ai's capabilities.
- The `ai.run` function is for controling the artificial inteligence which is build in for every module if there are datasets to build from, for this there will be an extra Guide.
- The `sensor` function is for controling the Input for the artificial inteligence.
- The `sleep` function will hold the programm for a few moments.
- The `log` function will print any value you give it.
- The `switch` function will wait on a Signsl from the push sensor.
- The `generate_ab` function will generate a function it self.
- The `call` function will call the generatet function.

## Artificial Neural Network

This AI is build in a way that integrates very good with the Spike Prime Enviroment.
For this AI I build a extra function so that you dont have to import any thing else accept the math lib.
First you have to initialise the Data_set in the Data list, secondly I defined the functions.
Please use the ai.run after youre `calibrate` function and give the values with `{"Calibration":calibration, "Akku":100%, "Wheelusage":0.95}`.

### Data Rules

Please get the values for the data List for your Robot for your self and dont use the example Data set.
For the calibration you can use the build in function `calibrate` thoese values will be printet please put them in youre Dataset.
You have to consider that the wheels degrade with every run about -0.05 Value.
The batterie loading Point has to be carefully read of the the [Official Spike Prime Software](https://education.lego.com/de-de/downloads/spike-app/software/) before the run.
If you do this min. 15 times you get a good value evaluation, the more Data you feed the AI the better.

```python
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
```

## Examples

The best way to learn the language you have to remeber the syntax and the functions but then you have to practice. The following code examples will show you how to begin after you have try'd it you can open the Examples.md file and learn more about the Spike Custom System Programming Language.

1. `drive(10)`
2. `module(100)`
3. `sensor(color)`
4. `ai.run(Data_values)`
5. `log(Hello World)`
6. `calibrate()`
7. `tank(30)`
8. `switch`
9. `ai.run({"Calibration" : calibration, "Akku" : 90, "Wheelusage" : 0.95})`
10. `generate_ab(new_function)`
11. `call(new_function)`

## Full example with explaination

At the beginning you have to initialize the functions with the `init()`, `variables.init()`, `ai.init()`, `module.init()`, `motor.init()`, `sensor.init()` and `calibration.init()` functions. After that you have to start the main loop with the `main()` function. In the main loop you can use the functions that are shown in [Functions](#functions). The following example shows a simple program that drives the robot forward, turns left, and then drives forward again.

```c
//(This is a simple example of a Spike Custom System Programming Language program. Without ai.)
init()
variable.init()
module.init()
motor.init()
sensor.init()
calibration.init()
ai.init()
log(Running main Function)
generate_ab(new_function)
log(running the new_function)
main.init()
switch()
calibrate()
ai.run({'Calibration': calibration, 'Akku': 85, 'Wheelusage': 0.95})
drive(10)
call(new_function)
switch()
tank(30)
switch()
drive(10)
main.run()
```

Out of that you become some Code in a .llsp3 file that you have to ether have to open with the official [desktop app](https://www.microsoft.com/store/productId/9NG9WXQ85LZM?ocid=pdpshare) from Lego or upload the file to the [Official Spike Prime Webapp](https://education.lego.com/de-de/downloads/spike-app/software/).

```python
# This is a simple example of a Spike Custom System Programming Language program.
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
ai_data = []

def write_ai_data(file):
    with open('{file}', 'w') as f:
        for line in ai_data:
            f.write(line)
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
```

The .llsp3 file you can put in the [Spike Prime Software](https://spike.legoeducation.com/) and then load on you're Spike Prime.

## Guide

1. First you have to run the programm then you see a menu with a few options:

![alt text](image-4.png)  ![alt text](image-5.png)

2. if you click on the both buttons that are pointet at you will come to the following menu that will let you chose the file that you want to compile or debug:

![alt text](image-6.png)

3. If you have chosen you`re file that will automaticly debug or compile the Programm, like in the cli version if you let it compile you're programm you get an .py file that you can copy in the offical [Spike Prime Software](https://spike.legoeducation.com/) and upload to you're Spike Prime.

## Robot Recomondations

This is important for the functionality of your robot:

1. please use the Spike Prime Hub.
2. You have to use the following Ports for your motors: Motorpair: F and B, Module Motor: E; A, Force Sensor: D, Distance Sensor: C.
3. You have to use the official [Spike Prime Software](https://spike.legoeducation.com/) for the deployment for the Spike Prime Hub.

## Conclusion

This guide has provided you with all the information you need to get started with programming in Spike Custom System Programming. If you have any questions or need further assistance, please refer to the official documentation or contact me.
Thank you for choosing Spike Custom System Programming! We hope you enjoy using our programming language and look forward to seeing what you create.

## License

[Apache License](http://www.apache.org/licenses/)
Version 2.0, January 2004

Aiirondev, 04.03.2024

## Contact

If you have any questions or need further assistance, please contact me at <iron.ai.dev@gmail.com>
