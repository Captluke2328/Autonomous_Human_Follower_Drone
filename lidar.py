import threading
import state
import serial
import time
import numpy as np

class Lidar(threading.Thread):
    def __init__(self,D, Alt):
        threading.Thread.__init__(self)
        
        self.daemon   = True
        self.engine   = D.engines
        self.altitude = Alt
        self.distance = 0
        
        self.ser = serial.Serial("/dev/ttyTHS1", 115200,timeout=0) # mini UART serial device
        if self.ser.isOpen() == False:
            self.ser.open()
            print("Port Opened")
            
    def run(self):
        #if (state.get_airborne()):
        while True: 
            counter = self.ser.in_waiting # count the number of bytes of the serial port
            if counter > 8:
                bytes_serial = self.ser.read(9) # read 9 bytes
                
                self.ser.reset_input_buffer() # reset buffer

                if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59: # check first two bytes
                    distance    = bytes_serial[2] + bytes_serial[3]*256 # distance in next two bytes
                    strength    = bytes_serial[4] + bytes_serial[5]*256 # signal strength in next two bytes
                    temperature = bytes_serial[6] + bytes_serial[7]*256 # temp in next two bytes
                    temperature = (temperature/8.0) - 256.0 # temp scaling and offset
                    self.distance    = distance/100.0
                    
                    #print(self.distance)
                    
                if (self.distance < 1) and (state.get_airborne() == "on"):
                    self.engine.executeChangesNow(-0.2,0,self.altitude)
                                
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
                    distance    = distance/100.0
                
                    if (distance < 1):
                        self.engine.executeChangesNow(-0.2,0,self.altitude)

    def read_lidar_distance(self):
        while True:
            counter = self.ser.in_waiting 
            if counter > 6:
                bytes_serial = self.ser.read(7) 
                self.ser.reset_input_buffer() 
                if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59: 
                    distance = bytes_serial[2] + bytes_serial[3]*256 
                    strength = bytes_serial[4] + bytes_serial[5]*256 
                    distance = distance/100.0
                    
                    if (distance < 1):
                        self.engine.executeChangesNow(-0.2,0,self.altitude)
                  
    # def read_distance(self):
    #     distance,strength,temperature = self.read_tfluna_data()
    #     return distance
