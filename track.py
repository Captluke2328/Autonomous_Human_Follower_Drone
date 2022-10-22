import logging, time, threading
import jetson.inference
import jetson.utils
import cv2
import numpy as np
import arduino as sm

#class Track(threading.Thread):
class Track:
    def __init__(self,cam):
        # threading.Thread.__init__(self)
        self.daemon = True
        self.w      = cam.DISPLAY_WIDTH
        self.h      = cam.DISPLAY_HEIGHT
        self.ser    = sm.initConnection('/dev/ttyACM0',9600)

    def trackobject(self,info,pid,pError):
        self.info   = info
        self.pid    = pid
        self.pError = pError
        
        if ((self.info[1]) !=0) and ((self.info[1]) < 500000):
            error = self.w//2 - self.info[0][0]
            self.posX   = int(self.pid[0]*error + self.pid[1]*(error-self.pError))
            self.posX   = int(np.interp(self.posX, [-self.w//4, self.w//4], [-35,35]))
            self.pError = error
            
            #print(str(self.posX) + " " + str(info[1]))
            sm.sendData(self.ser, [50,self.posX],4)
            
        # elif ((info[1]) !=0) and ((info[1]) > 5760000):
        #     sm.sendData(self.ser,[0,0],4)
        
        else:
            #pass
            sm.sendData(self.ser,[0,0],4)
        
    def visualise(self,img):
         # Top
        cv2.rectangle(img, (0,0), (self.w,24), (0,0,0), -1)

        # Bottom
        cv2.rectangle(img, (0, self.h-24), (self.w,self.h), (0,0,0), -1)
        
         # Width and Height
        text_dur = 'Width : {} Height: {}'.format(self.w, self.h)
        cv2.putText(img, text_dur, (10,16), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (150,150,255), 2)
        
        
            
        
            
        
    

