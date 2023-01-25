from dronekit import *
from pymavlink import mavutil
from time import sleep
from engines import *
import numpy as np
import state
from simple_pid import PID

class controlTab:
    def __init__(self,D):
        self.vehicle = D.vehicle
        self.drone = D
        self.THRESHOLD_ALT = 0.3
        self.engine = D.engines
        
        self.inputValueYaw = 0
        
        self.MAX_SPEED = 4       # M / s
        self.MAX_YAW = 15  
        
        self.USE_PID_YAW = True
        self.USE_PID_ROLL = False
                
        self.P_YAW = 0.02 #orgineel 0.01
        self.I_YAW = 0
        self.D_YAW = 0 
        
        self.P_ROLL = 0.22
        self.I_ROLL = 0
        self.D_ROLL = 0
        
        self.pidYaw = None
        
    def configure_PID(self):
        
        """ Creates a new PID object depending on whether or not the PID or P is used """ 
        self.pidYaw = PID(self.P_YAW, self.I_YAW, self.D_YAW, setpoint=0)       # I = 0.001
        self.pidYaw.output_limits = (-self.MAX_YAW, self.MAX_YAW)               # PID Range
        #self.pidRoll = PID(self.P_ROLL, self.I_ROLL, self.D_ROLL, setpoint=0)   # I = 0.001
        #self.pidRoll.output_limits = (-self.MAX_SPEED, self.MAX_SPEED)          # PID Range
        print("Configuring PID")
  
    def armAndTakeoff(self,altitude):
        print("Setting ground speed to 3")
        self.vehicle.groundspeed = 3
        
        print("Basic pre-arm checks")
        
        while not self.vehicle.is_armable:
            print("waiting for vehicle to initialize")
            time.sleep(1)
            
        print("Arming Motors")
        
        self.vehicle.mode  = VehicleMode("GUIDED")
        self.vehicle.armed = True
        
        while not self.vehicle.armed:
            print("waiting for arming...")
            time.sleep(1)
        
        print("Taking off")
        self.vehicle.simple_takeoff(altitude)
        
        while True:
            #print (" Altitude: ", self.vehicle.location.global_relative_frame.alt)
            if self.vehicle.location.global_relative_frame.alt>=altitude*0.95:
                #print ("Reached target altitude")
                break
            time.sleep(1)
            
    def land(self):
        print("Landing")
        self.vehicle.channels.overrides = {}
        self.vehicle.mode = VehicleMode("LAND")
        state.set_system_state("end")

    def goHome(self):
        print('Going Home')
        self.vehicle.mode = VehicleMode("RTL")
        
    def stop_drone(self,altitude):
        self.engine.send_movement_command_YAW(0)
        self.engine.executeChangesNow(0, 0, 0)
        
    def set_XDelta(self, xDelta):
        self.inputValueYaw = xDelta
    
    def control_drone(self):
        if self.inputValueYaw == 0:
            self.engine.send_movement_command_YAW(0)
        
        else:
            self.movementYawAngle = (self.pidYaw(self.inputValueYaw) * -1)
            self.engine.send_movement_command_YAW(self.movementYawAngle)
        
