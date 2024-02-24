#mode for the run
mode = 0


#from _typeshed import SupportsWrite
import force_sensor, distance_sensor, motor, motor_pair
from hub import port
from app import linegraph as ln
import runloop
from math import *
import time
#import numpy # AI/KNN

#Variables
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

#Calibrate function
async def calibrate(new=1, speed=1000, acceleration=1000):
    if (new == 1):
        if (distance_sensor.distance(port.C) < 110):
            print("Calibration not possible! | Distance to small!")
        elif (distance_sensor.distance(port.C) > 110):
            try:
                await drive(-1, 14, speed, acceleration)
                distance0 = distance_sensor.distance(port.C)
                await drive(10, 14, speed, acceleration)
                distance1 = distance_sensor.distance(port.C)
                calibration = distance0 - distance1
                #print("Calibration done!")
                print(calibration)
                wait(0.5)
            except:
                print("Calibration not possible! | Error!")
    elif (new == 0):
        calibration = average
        await drive(10, 14, speed, acceleration)
    elif (new == 2):
        if await switch():
            while times <= 10:
                times + 1
                print(times)
                print("-----------------")
                if (distance_sensor.distance(port.C) < 110):
                    print("Calibration not possible! | Distance to small!")
                elif (distance_sensor.distance(port.C) > 110):
                    try:
                        await drive(-1, 14, speed, acceleration)
                        distance0 = distance_sensor.distance(port.C)
                        await drive(10, 14, speed, acceleration)
                        distance1 = distance_sensor.distance(port.C)
                        calibration = distance0 - distance1
                        #print("Calibration done!")
                        print(calibration)
                        average_calibration.append(calibration)
                        wait(0.5)
                    except:
                        print("Calibration not possible! | Error!")
                print("-----------------")
            calibration = (average_calibration[0] + average_calibration[1] + average_calibration[2] + average_calibration[3] + average_calibration[4] + average_calibration[5] + average_calibration[6] + average_calibration[7] + average_calibration[8] + average_calibration[9]) / 10
            print("Durchschnitt:")
            print(calibration)
    else:
        print("Bist du dumm?")

#Drive function
async def drive(distance=0, multiplier=14, speed=1000, acceleration=1000):
    if (distance > 0):
        degrees = multiplier*(distance - calibration)
        await motor_pair.move_for_degrees(pair, degrees, 0, velocity=speed, acceleration=acceleration)
    elif (distance < 0):
        degrees = multiplier*(distance + calibration)
        await motor_pair.move_for_degrees(pair, degrees, 0, velocity=speed, acceleration=acceleration)
    elif (distance == 0):
        print("Bist du dumm?")

#Tank function
async def tank(degrees=0, left_speed=1000, right_speed=1000, acceleration=1000):
    #180 degrees = 90 Grad
    if (degrees > 0):
        await motor_pair.move_tank_for_degrees(pair, -degrees, left_speed, -right_speed, acceleration=acceleration)
    elif (degrees < 0):
        await motor_pair.move_tank_for_degrees(pair, degrees, -left_speed, right_speed, acceleration=acceleration)
    elif (degrees == 0):
        print("Bist du dumm?")

#Obstacle function
async def obstacle(distance=0, speed=1000, acceleration=1000):
    if (distance > 0):
        while distance_sensor.distance(port.C) > distance:
            await drive(2, 14, speed, acceleration)
        print("Obstacle detected!")
        #print(distance_sensor.distance(port.C))
    elif (distance <= 0):
        print("Bist du dumm?")

#Module function
async def module(degrees=0, speed=1110, acceleration=10000):
    if (degrees > 0):
        await motor.run_for_degrees(motor_module, degrees, speed, acceleration=acceleration)
    elif (degrees < 0):
        await motor.run_for_degrees(motor_module, degrees, speed, acceleration=acceleration)
    elif (degrees == 0):
        print("Bist du dumm?")

async def module1(degrees=0, speed=1110, acceleration=10000):
    if (degrees > 0):
        await motor.run_for_degrees(motor_module1, degrees, speed, acceleration=acceleration)
    elif (degrees < 0):
        await motor.run_for_degrees(motor_module1, degrees, speed, acceleration=acceleration)
    elif (degrees == 0):
        print("Bist du dumm?")

#Switch function
async def switch(switch=False):
    while switch == False:
        if (force_sensor.force(force_module) >= 50):
            switch = True
            return True

#Wait function
def wait(time0):
    time.sleep(time0)



# (c) Maximilian Gründinger 2024
#
#
#AI Stuff Start
#
#
#
ai_data_1 = [
    (5, 8),
    (4, 9),
    (6, 7),
    (7, 6),
    (2, 11),
    (1, 12),
    (8, )
]

def ai_enforcement(data, prediction, modus): # This Linear Regression KNN System is codet by Maximilian Gründinger 
    # Regressives KNN supervised learning Programm für gewählte parameter vom abstandt sensor abgleich mit dem input
    # the data / enforcement an wichtigen und ungenauen stellen einbauen
    # Robot dataset
    print("Running")
    # Thge Data is consisting of the (expectet value, measured value) of the distance / tilt of the robot depens on sitiuations
    robot = [
        (0.0380759, 233),
        (-0.00188202, 91),
        (0.0852989, 111),
        (-0.0890629, 152),
        (0.00538306, 120),
        (-0.0926955, 67),
        (0.04534098, 310),
        (0.0631845, 94),
        (-0.0277622, 183),
        (0.0633294, 66),
    ]

    if data != None:
        data_ai = data.copy()
        if type(data_ai) is str:
            print("wrong Data Type: String was given, expectet List!")
        if type(data_ai) is bool:
            print("wrong Data Type: Boolean was given, expectet List!")
        if type(data_ai) is tuple:
            print("wrong Data Type: Tuple was given, expectet List!")
        if type(data_ai) is float:
            print("wrong Data Type: Float was given, expectet List!")
        if type(data_ai) is list:
            robot = [data_ai]
    else:
        print("No Data Input was Given! | AI can't work! (The Output is an Fixed Test Dataset!)")

    # Extract input and target values
    robot_X = [x[0] for x in robot]
    robot_y = [x[1] for x in robot]

    # Split the data into training/testing sets
    robot_X_train = robot_X[:-4]
    robot_X_test = robot_X[-4:]

    robot_y_train = robot_y[:-4]
    robot_y_test = robot_y[-4:]

    # Create linear regression object (coefficient calculation)
    def simple_linear_regression(x, y):
        n = len(x)
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        xy_mean = sum([x[i] * y[i] for i in range(n)]) / n
        x_sq_mean = sum([x[i] ** 2 for i in range(n)]) / n

        m = (xy_mean - x_mean * y_mean) / (x_sq_mean - x_mean ** 2)
        b = y_mean - m * x_mean

        return m, b

    m, b = simple_linear_regression(robot_X_train, robot_y_train)

    # Input data
    print('Input Values')
    print(robot_X_test)

    # Make predictions using the testing set
    robot_y_pred = [m * x + b for x in robot_X_test]

    def print_robot_dataset(robot_X_train, robot_y_train, robot_X_test, robot_y_test, robot_y_pred):
        print('Robot dataset')
        print('Legend: Blue - Test data, Red - Predicted data, Black - Training data')

        # Print training data
        print('\nTraining data:')
        for x, y in zip(robot_X_train, robot_y_train):
        #    print(f'Input: {x}, Actual: {y}')
            pass

        # Print test data
        print('\nTest data:')
        for x, y, y_pred in zip(robot_X_test, robot_y_test, robot_y_pred):
            pass
        #    print(f'Input: {x}, Actual: {y}, Predicted: {y_pred}')

        # Create ASCII graph
        max_value = max(max(robot_y_train), max(robot_y_test), max(robot_y_pred))
        min_value = min(min(robot_y_train), min(robot_y_test), min(robot_y_pred))

        for i in range(max_value, min_value - 1, -1):
            row = ''
            for x_train, y_train, y_test, y_pred in zip(robot_X_train, robot_y_train, robot_y_test, robot_y_pred):
                if y_train >= i:
                    row += 'B'# B for Black (Training data)
                elif y_test >= i:
                    row += 'O'# O for Blue (Test data)
                elif y_pred >= i:
                    row += 'R'# R for Red (Predicted data)
                else:
                    row += ' '# Empty space
            print(row)

        # Legend
        print('\nLegend:')
        print('B - Training data, O - Test data, R - Predicted data')

    # Predicted Data
    print("Predicted Output Values")
    print(robot_y_pred)
    if modus == "running":
        return robot_y_pred
    elif modus == "testing":
        print_robot_dataset(robot_X_train, robot_y_train,robot_X_test, robot_y_test,robot_y_pred)

    print("Ende")

#
#
#
#End AI Stuff
#
#
# (c) Maximilian Gründinger 2024


# Code
async def bewegungs_studie():
    pass
async def kino():
    await module(50)
    await drive(18)
    await module(-330)
    await drive(-19)

async def music():
    await drive(2)
    await tank(-90)
    await drive(20)
    await tank(30)
    await drive(9)
    await module1(200)
    await drive(10)
    await module(-200)
    await drive(-40)

async def szenenwechsel(mode = 1):
    async def drop():
        await module1(100)
        await module1(-200)
        await drive(4)
    if mode == 1:
        await drive(-2)
        await drive(5)
        await tank(-90)
        await drive(50, 7, 500)
        await tank(90)
        await drive(43, 14, 500)
        await drive(2)
        await drive(-8, 14, 500)
        wait(0.5)
        await drive(9, 14, 500)
        await drive(-9)
        await tank(-170)
        await drive(20)
        await drop()
        await drop()
        await drive(-36)
        await tank(110)
        await drive(-12)
        await tank(80)
        await drive(11)
        await drop()
        await drop()
        await drive(-8)
        await drive(-7)
        await tank(-90)
        await drive(-20)
        await tank(20)
        await drop()
        await tank(-30)
        await drive(-40)
        #await tank(-42)
        #await drive(-40)
        #await tank(-90)
        #await drive(-25)
    else:
        if await switch():
            while times1 <= 10:
                times1 + 1
                print(times1)
                print("-----------------")
                await drive(5)
                await tank(-90)
                await drive(27)
                await tank(92)
                await drive(20)
                await obstacle(242)
                print(distance_sensor.distance(port.C))
                print("-----------------")
            obs = (average_obs[0] + average_obs[1] + average_obs[2] + average_obs[3] + average_obs[4] + average_obs[5] + average_obs[6] + average_obs[7] + average_obs[8] + average_obs[9]) / 10
            print("Durchschnitt:")
            print(obs)

async def filmset():
    await drive(7)
    await tank(-180)
    await drive(50)
    await module(-1900)
    await drive(-15)
    await tank(95)
    await drive(1)
    await module(1630)
    await tank(-95)
    await drive(-26)
    await tank(45)
    await drive(-6)

async def erlebnis():
    await drive(49, 7)
    await tank(-180)
    await drive(126, 7)
    await tank(180)
    await drive(59, 7)
    await tank(90)
    await drive(14, 7)
    await tank(-90)
    await drive(13, 7)
    await module(-2000)
    await module(2000)

async def konzert():
    await drive(-54, 1)
    await tank(-180)
    await drive(60)
    await tank(15)
    await drive(30)
    await tank(100)
    await drive(15)
    await drive(-10)
    await tank(-250)
    await drive(70, 14, 1050, 10000)

async def druckmaschine():
    await drive(11, 7)
    await tank(105)
    await drive(30)
    await tank(-24)
    await drive(16, 14, 500)
    await drive(-3)
    await tank(45)
    await module(-1000)
    await drive(-7)
    await module(600)
    await drive(-4)
    await module(500)
    await drive(-10)
    await tank(80)
    await drive(27)
    await tank(-120)
    await drive(7)
    await module(-800)
    await drive(-20)
    await tank(90)
    await drive(-50)

async def blume():
    await drive(42)
    await tank(300, 10, 525)
    await drive(26)
    await tank(35)
    await drive(49, 7)
    await tank(-250, 1000, 50)
    await drive(10)
    await drive(-2)
    await tank(-100, 0, 1000)
    await drive(-7, 7)
    await module(150)
    await drive(-6)
    await tank(-180)
    #await module(-120)
    await drive(53)
    await tank(-168)
    await drive(70)

async def achterbahn():
    await drive(4)
    await tank(192)
    await drive(40)
    await module(1300)
    await drive(-15)
    await drive(-40)

async def tower():
    await drive(42)
    await tank(300, 10, 525)
    await drive(26)
    await tank(35)
    await drive(97, 7)
    await tank(185)
    await drive(7)
    await module(1700)
    await drive(-8)
    await tank(180)

async def lichtshow():
    await drive(69)

#Datensameln
async def main1():
    if await switch():
        await calibrate(2)
        await kino()
    #if await switch():
    #    await music()
    if await switch():
        await szenenwechsel(0)
    #if await switch():
    #    await zuschauer()
    if await switch():
        await filmset()
    if await switch():
        await erlebnis()
        await konzert()
    if await switch():
        await druckmaschine()
    if await switch():
        await achterbahn()
    if await switch():
        await blume()
    if await switch():
        await tower()
    if await switch():
        await lichtshow()
    print("done!")

async def main0():
    #if await switch():
    #   await calibrate(0)
    #   await kino()
    #if await switch():
    #    await music()
    #if await switch():
    #   await szenenwechsel(1)
    #if await switch():
    #    await filmset()
    #if await switch():
    #    await erlebnis()
    #    await konzert()
    if await switch():
        await druckmaschine()
    if await switch():
        await achterbahn()
    if await switch():
        await blume()
    if await switch():
       await tower()
    #if await switch():
    #    await lichtshow()
    print("done!")

print("running...")
if (mode == 1): 
    runloop.run(main1())
elif (mode == 0):
    runloop.run(main0())
else:
    print("Bist du dumm?")