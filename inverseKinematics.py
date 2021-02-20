from control import sendOrder, serialPort, order

import tinyik

import numpy as np

arm = tinyik.Actuator(["z",[0,0,75],"y",[0,0,125],"y",[0,0,125],"y",[0,0,60]])

target = [0,0,385]

solver2robot = np.vectorize(lambda x: (x+90)%360)

def targetToAngles(x,y,z):
    arm.ee = [x,y,z]
    return solver2robot(np.rad2deg(arm.angles)) # Returns a 1-D array with all four angles that will take the robot's hand to the coordinates (x,y,z)

if __name__ == "__main__":
    userInput = "Nothing"
    while userInput != "":
        userInput = input("")
        for coord,token in enumerate(userInput.split()):
            target[coord] = int(token)
        arm.ee = target
        if serialPort.is_open:
            angles : np.array = solver2robot(np.rad2deg(arm.angles))
            sendOrder(np.append(angles,90,73))
