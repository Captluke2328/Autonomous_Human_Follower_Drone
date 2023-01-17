from dronekit import *
from pymavlink import mavutil
from time import sleep
from engines import *
import numpy as np
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
        
    def goHome(self):
        print('Going Home')
        self.vehicle.mode = VehicleMode("RTL")
        
    def stop_drone(self):
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
        
    # def yaw(self,cx,cy):
    #     print("Tracking")
    #     self.engine_imp.send_movement_command_YAW(cx)
        
    # def armAndTakeoff(self):
    #     @self.vehicle.on_attribute('mode')
    #     def mode_callback(self,attr_name,value):
    #         print(f">> Mode Update: {value} ")

    #     # We will not let the script to continue unless it changes to GUIDED
    #     self.vehicle.mode = VehicleMode("GUIDED")
    #     while not self.vehicle.mode.name == "GUIDED":
    #         sleep(1)
        
    #     if (self.vehicle.mode.name == "GUIDED"):
    #         if not self.vehicle.armed:
    #             self.vehicle.armed = True
                
    #             if (self.vehicle.location.global_relative_frame.alt < self.THRESHOLD_ALT):
    #                 takeoff_alt = 5
    #                 self.vehicle.simple_takeoff(takeoff_alt)
    #                 while self.vehicle.location.global_relative_frame.alt < (takeoff_alt - self.THRESHOLD_ALT):
    #                     sleep(0.3)
    #                 self.takeoff = True
    #             else:
    #                 if (self.vehicle.location.global_relative_frame.alt > self.THRESHOLD_ALT):
    #                     self.vehicle.mode = VehicleMode("LAND")     
    #         else:
    #             # Disarm if landed
    #             if (self.vehicle.location.global_relative_frame.alt < self.THRESHOLD_ALT):
    #                 self.vehicle.armed = False

    # def right(self):
    #     x,y = 0.0, 2.0 
    #     yaw = self.vehicle.attitude.yaw
    #     self.engine_imp.send_global_velocity(
    #         x * np.cos(yaw) - y * np.sin(yaw),
    #         x * np.sin(yaw) + y * np.cos(yaw),
    #         0,
    #         2,      
    #     )
    #     self.engine_imp.send_global_velocity(0,0,0,1)

    # def left(self):
    #     x,y = 0.0, -2.0 
    #     yaw = self.vehicle.attitude.yaw
    #     self.engine_imp.send_global_velocity(
    #         x * np.cos(yaw) - y * np.sin(yaw),
    #         x * np.sin(yaw) + y * np.cos(yaw),
    #         0,
    #         2,       
    #     )
    #     self.engine_imp.send_global_velocity(0,0,0,1)

    # # Go Back
    # def backward(self):
    #     print("Backward...")
    #     x, y = -2.0, 0.0  # meters
    #     yaw = self.vehicle.attitude.yaw
    #     self.engine_imp.send_global_velocity(
    #         x * np.cos(yaw) - y * np.sin(yaw),
    #         x * np.sin(yaw) + y * np.cos(yaw),
    #         0,
    #         2, 
    #     )
    #     self.engine_imp.send_global_velocity(0, 0, 0, 1)
            
    # # Go Front
    # def forward(self):
    #     print("Forward...")
    #     x, y = 2.0, 0.0  # meters
    #     yaw = self.vehicle.attitude.yaw
    #     self.engine_imp.send_global_velocity(
    #        x * np.cos(yaw) - y * np.sin(yaw),
    #        x * np.sin(yaw) + y * np.cos(yaw),
    #        0,
    #        2, 
    #     )
    #     self.engine_imp.send_global_velocity(0, 0, 0, 1)
        
    # def stop(self):
    #     #print("Stop movement")
    #     x,y,z = 0,0,0
    #     self.engine_imp.send_global_velocity(
    #     x,
    #     y,
    #     z,
    #     2, 
    #     )
    #     self.engine_imp.send_global_velocity(0, 0, 0, 1)
    
    
    # def stopMovement(self):
    #     self.speed_x = 0
    #     self.speed_y = 0
    #     self.speed_z = 0
    #     self.engine_imp.executeChangesNow()
    
    # # Yaw Left   
    # def rotateLeft(self,angle):
    #     #self.engine.rotate(-1,angle)
    #     print("rotate Left----")
    
    # # Yaw Right
    # def rotateRight(self, angle):
    #     #self.engine.rotate(1, angle)
    #     print("rotate Right----")