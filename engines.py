import time, threading, logging
from dronekit import VehicleMode, Command
from pymavlink import mavutil
from time import  sleep

class Engines:
    def __init__(self,D):
        self.daemon = True
        self.vehicle = D.vehicle
        self.control = D

        #print("Engine has started-------", self.vehicle)
                    
    def executeChangesNow(self,velocity_x, velocity_y, altitude):

        #velocity_x positive = forward. negative = backwards
        #velocity_y positive = right. negative = left
        #velocity_z positive = down. negative = up (Yes really!)

        #print("Sending XYZ movement command with v_x(forward/backward): %f v_y(right/left): %f " % (velocity_x,velocity_y))

        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
        0,      
        0, 0,    
        mavutil.mavlink.MAV_FRAME_BODY_NED,  #relative to drone heading pos relative to EKF origin
        0b0000111111000111,  # original bit -> 0b0000111111000111, #ignore velocity z and other pos arguments # 0b0000111111100011
        0, 0, altitude,
        velocity_x, velocity_y, 0, 
        0, 0, 0, 
        0, 0)    

        self.vehicle.send_mavlink(msg)
        
    def send_movement_command_YAW(self,heading):
        direction = 1 #direction -1 ccw, 1 cw   
         
        msg = self.vehicle.message_factory.command_long_encode(
        0, 0,       
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, 
        0,          
        abs(heading),    
        0,      #speed deg/s
        1 if heading > 0 else -1,
        1,          #relative offset 1
        0, 0, 0)    

        self.vehicle.send_mavlink(msg)
        #Vehicle.commands.flush()
    
        