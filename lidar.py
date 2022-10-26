import serial,time
import numpy as np

class Lidar:
    def __init__(self):
        self.ser = serial.Serial("/dev/ttyTHS1", 115200,timeout=0) # mini UART serial device
        if self.ser.isOpen() == False:
            self.ser.open()
            print("Port Opened")
    
    def read_tfluna_data(self):
        while True:  
            counter = self.ser.in_waiting # count the number of bytes of the serial port
            if counter > 8:
                bytes_serial = self.ser.read(9) # read 9 bytes
                
                self.ser.reset_input_buffer() # reset buffer

                if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59: # check first two bytes
                    distance = bytes_serial[2] + bytes_serial[3]*256 # distance in next two bytes
                    strength = bytes_serial[4] + bytes_serial[5]*256 # signal strength in next two bytes
                    temperature = bytes_serial[6] + bytes_serial[7]*256 # temp in next two bytes
                    temperature = (temperature/8.0) - 256.0 # temp scaling and offset
                    return distance/100.0,strength,temperature

    def read_distance(self):
        distance,strength,temperature = self.read_tfluna_data()
        return distance

if __name__ == "__main__":
    init = Lidar()
    while True:
        x = init.read_distance()
        print(x)
