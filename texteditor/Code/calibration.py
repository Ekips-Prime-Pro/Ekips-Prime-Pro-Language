#Calibrate function
async def calibrate(speed=1000, acceleration=1000):
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
