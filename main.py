import cv2
import sys
import os
import threading
import state

from time import sleep,time

from detect import *
from camera import *
from track import *
from config import *

os.system ('sudo systemctl restart nvargus-daemon')

def takeoff():
    drone.control_tab.armAndTakeoff()
    state.set_system_state("search")
    
def search(info):
    start = time.time()
    drone.control_tab.stop_drone()
    while time.time() - start < 40:
        if (info[1]) != 0:
            state.set_system_state("track")
    state.set_system_state("land")
    
def track(info):
    if (info[1]) != 0:
        det.track.trackobject(info)
    else:
        state.set_system_state("search")
    
if __name__ == "__main__":
    cam = Camera()
    det = Detect(cam) 
    
    state.set_system_state("takeoff")

    while True:
        try:
            drone = Drone()
            break
        
        except Exception as e:
            print(str(e))
            sleep(2)
            
    while drone.is_active:
        try:       
            img,info = det.captureimage()   
            det.track.visualise(img)    
            
            if (state.get_system_state() == "takeoff") and (drone.control_tab.takeoff==False):
                off = threading.Thread(target=takeoff)
                off.start()
            
            elif(state.get_system_state() == "search") and (drone.control_tab.takeoff):
                sea = threading.Thread(target=search, args=(info,))
                sea.start()
                
            elif(state.get_system_state() == "track") and (drone.control_tab.takeoff):
                tra = threading.Thread(target=track, args=(info,))
                tra.start()
            
            elif(state.get_system_state() == "land"):
                drone.control_tab.land()
                sys.exit(0)
                      
            cv2.imshow("Capture",img)
            
            if cv2.waitKey(1) & 0XFF == ord('q'):
                break
        except Exception as e:
            print(str(e))
            
    cv2.destroyAllWindows()
        
        
    