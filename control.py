from typing import Any
import serial
from serial.tools import list_ports

import time


class OrderSender:
    ordersNames = {"Base": 0, "Shoulder": 1, "Elbow": 2,
                   "Wrist vertical": 3, "Wrist rotate": 4, "Grab": 5}

    def __init__(self, port: serial.Serial) -> None:
        self._order = [90, 90, 90, 90, 90, 73]
        self._port = port
        self._baseOffset=0
        assert self._port.isOpen(), f"Error, port given is not open"

    def send(self):
        self._port.write(
            bytes(f"{';'.join([str(token) for token in self._order])}\n", "utf-8"))

    def setServo(self, index: int, value: int):
        self._order[index] = value

    def __setattr__(self, name: str, value: Any) -> None:
        if name in OrderSender.ordersNames.keys():
            self._order[OrderSender.ordersNames[name]] = value
        else:
            self.__dict__[name] = value

    def setBaseOffset(self,value:int):
        self._baseOffset = value

    def sendCSV(self, file, frameLength: float = 0.1):
        """
        Sends one line of opened file file, every frameLength seconds.
        Each line of the file must contain integers inside a valid servo angle range
        These integers must be separated by a semi-colon (separator argument is for another version)
        """
        starttime = time.time()
        for idx, line in enumerate(file):
            for servoIdx, token in enumerate(line.split(";")):
                if servoIdx == 0:
                    self.setServo(servoIdx,int(token)+self._baseOffset)
                else:
                    self.setServo(servoIdx, int(token))
            self.send()
            print(f"Sent frame {idx+1}")
            # Wait a few milliseconds before sending the next order
            time.sleep(frameLength - ((time.time() - starttime) % frameLength))


def choosePort():
    print("Here are all available ports. Please enter the index of the port you'd like to open\n")
    allPorts = list_ports.comports(include_links=False)
    for idx,port in enumerate(allPorts):
        print(f"{idx} : {port.name}")
    userChoice = input()
    if userChoice.isnumeric():
        return allPorts[userChoice].name
    else:
        return userChoice


serialPort = serial.Serial(choosePort(), 115200)

orderSender = OrderSender(serialPort)


def playModeRawOrders():
    """Raw servo orders (in the form Base Shoulder Elbow Wrist_vertical Wrist_rotate Grab, in degrees)"""
    userInput = input("")
    while userInput != "":
        for place, token in enumerate(userInput.split()):
            if token.isnumeric():
                orderSender.setServo(place,int(token))
                print(orderSender._order)
        orderSender.send()
        userInput = input("")


def playModeCSVAnimation():
    """Choose a CSV file with bone rotations keyframes"""
    userInput = input(
        "Please enter the name of the CSV file you'd like to send")
    file=open(userInput)
    baseOffset = int(input("Please enter the angle offset (in degrees) for the robot's base (0 if you don't know what this means)"))
    orderSender.setBaseOffset(baseOffset)
    orderSender.sendCSV(file,0.04)


playModes = {1: playModeRawOrders,
             2: playModeCSVAnimation}

if __name__ == "__main__":
    print("Welcome to this robot control script\n")
    print("Please choose an option from the menu below\n")
    for k, v in playModes.items():
        print(f"{k} : {v.__doc__}", end="\n")
    selection = int(input(""))
    if selection not in playModes:
        print("Menu entry does not exist. Good bye !")
    else:
        playModes[selection]() # Go to the selected play mode
