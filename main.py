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

pError   = 0
pid      = [0.3,0.0]
#pid     = [0.5,0.4]

def takeoff():
    drone.control_tab.armAndTakeoff()
    state.set_system_state("search")
    
def search(info):
    start = time.time()
    drone.control_tab.stop_drone()
    while time.time() - start < 60:
        if (info[1]) != 0:
            state.set_system_state("track")
    state.set_system_state("land")
    
def track(info,drone):
    print(info[1])
    if (info[1]) != 0:
        det.track.trackobject(info,pid,pError)
    else:
        state.set_system_state("search")
    
if __name__ == "__main__":
  

    while True:
        try:
            drone = Drone()
            break
        
        except Exception as e:
            print(str(e))
            sleep(2)
            
    cam = Camera()
    det = Detect(cam,drone)
    drone.control_tab.configure_PID()
    
    state.set_system_state("takeoff")

    while drone.is_active:
        try:       
            img,info = det.captureimage()   
            det.track.visualise(img)    
            
            if (state.get_system_state() == "takeoff"):
                off = threading.Thread(target=takeoff)
                off.start()
            
            elif(state.get_system_state() == "search"):
                sea = threading.Thread(target=search, args=(info,))
                sea.start()
                
            elif(state.get_system_state() == "track"):
                tra = threading.Thread(target=track, args=(info,drone))
                tra.start()
            
            elif(state.get_system_state() == "land"):
                drone.control_tab.land()
                cv2.destroyAllWindows()
                break
                #sys.exit(0)
                
            print(state.get_system_state())
                      
            cv2.imshow("Capture",img)
            
            if cv2.waitKey(1) & 0XFF == ord('q'):
                break
        except Exception as e:
            print(str(e))
            
    cv2.destroyAllWindows()
        
        
    