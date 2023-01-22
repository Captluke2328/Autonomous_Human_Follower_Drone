import jetson.inference
import jetson.utils
import cv2
import numpy as np
from engines import *

#class Track(threading.Thread):
class Track:
    def __init__(self,cam,D):
        # threading.Thread.__init__(self)
        self.daemon  = True
        self.w       = cam.DISPLAY_WIDTH
        self.h       = cam.DISPLAY_HEIGHT  
        self.engine  = D.engines 
        self.control = D.control_tab
        #self.lidar   = D.lidar
     
    def trackobject(self,info,pid,pError,altitude):
        self.info   = info
        self.pid    = pid
        self.pError = pError
        
        if ((self.info[1]) !=0): # and ((self.info[1]) < 50004):
            error = self.w//2 - self.info[0][0]
            self.posX   = int(self.pid[0]*error + self.pid[1]*(error-self.pError))
            #self.posX  = int(np.interp(self.posX, [-self.w//4, self.w//4], [-35,35]))
            
            # 2nd Option
            #self.posX  = int(np.interp(self.posX, [-self.w//4, self.w//4], [-15,15]))
            
            # 1st Option
            self.posX   = int(np.clip(self.posX, -15,15))
               
            self.pError = error
            
            #print(str(self.posX) + " " + str(info[1]))
            
            self.engine.executeChangesNow(0.2,0,altitude)
            self.engine.send_movement_command_YAW(self.posX)
            
            # 1st Method of PID
            #self.control.set_XDelta(self.posX)
            #self.control.control_drone()
         
       # elif ((info[1]) !=0) and ((info[1]) > 51104):
       #     self.engine.executeChangesNow(-0.2,0,2.5)
                       
        else:
            self.engine.executeChangesNow(0,0,altitude)
            self.engine.send_movement_command_YAW(0)
            
            # 1st Method of PID
            #self.control.set_XDelta(0)
            #self.control.control_drone()
           
        #print(self.lidar.read_distance())
        
    #def distance(self):
    #    self.distance = self.lidar.read_distance()
        
    def visualise(self,img):
         # Top
        cv2.rectangle(img, (0,0), (self.w,24), (0,0,0), -1)

        # Bottom
        cv2.rectangle(img, (0, self.h-24), (self.w,self.h), (0,0,0), -1)
        
         # Width and Height
        text_dur = 'Width : {} Height: {}'.format(self.w, self.h)
        cv2.putText(img, text_dur, (10,16), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (150,150,255), 2)
        
        

        
            
        
    

