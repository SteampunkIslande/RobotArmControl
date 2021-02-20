import serial
from serial.tools.list_ports import comports

if __name__ == "__main__":
    ports = {k:v.device for k,v in enumerate(comports())}
    print("Available ports:\n")
    for k,v in ports.items():
        print(f"{k}:{v}\n")
    portIndex = input("Please select the index of the port you want to communicate with\n")
    baudRate = input("Please choose the baud rate\n")
    socket = serial.Serial(ports[int(portIndex)],baudRate)
    if socket.is_open:
        print(f"Successfully opened serial port on {socket.name}\nYou can now start sending bytes to the port\n")
        while True:
            while socket.in_waiting>0:
                print(socket.read_all(),end="")
            socket.write(bytes(input(""),"utf-8"))