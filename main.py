import cv2
import sys
import os
import threading
import state

from time import sleep,time
from datetime import datetime

from detect import *
from camera import *
from track import *
from config import *
from lidars import *

#os.system ('sudo systemctl restart nvargus-daemon')
#os.system ('sudo chmod 666 /dev/ttyTHS1')

pError   = 0

# 1st Option 
#pid      = [0.1,0.1]

# 2nd Option
pid     = [0.3,0.1]

#pid     = [0.5,0.4]

def takeoff():
    drone.control_tab.armAndTakeoff()
    state.set_system_state("search")
    
def search(id):
    start = time.time()
    drone.control_tab.stop_drone()
    while time.time() - start < state.get_time():
        if (id == 1):
            state.set_system_state("track")
    state.set_system_state("land")
    
def track(info,drone):
    #print(info[1])
    if (info[1]) != 0:
        state.set_airborne("on")
        det.track.trackobject(info,pid,pError)
        
    else:
        state.set_system_state("search")
        state.set_time(60)

# def distance():
#     lidar.read_lidar_distance()

if __name__ == "__main__":
    
    while True:
        try:
            drone = Drone()
            break
        
        except Exception as e:
            print(str(e))
            sleep(2)
        
    cam = Camera()
    curr_timestamp = int(datetime.timestamp(datetime.now()))

    path = "/home/jlukas/Desktop/My_Project/Autonomous_Human_Follower_Drone/record/"
    writer= cv2.VideoWriter(path + "record" + str(curr_timestamp) + '.mp4', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30 ,(cam.DISPLAY_WIDTH,cam.DISPLAY_HEIGHT))

    det   = Detect(cam,drone)
    
    lidar = Lidars(drone)
    lidar.start()

    drone.control_tab.configure_PID()

    state.set_system_state("takeoff")
    state.set_airborne("off")

    while drone.is_active:
        try:       
            img, id, info = det.captureimage()   
            det.track.visualise(img)    
            
            #print(info[1])
            
            if (state.get_system_state() == "takeoff"):
                off = threading.Thread(target=takeoff)
                off.start()
            
            elif(state.get_system_state() == "search"):
                state.set_time(60)
                sea = threading.Thread(target=search, args=(id,))
                sea.start()
                
            elif(state.get_system_state() == "track"):
                state.set_time(120)
                tra = threading.Thread(target=track, args=(info,drone))
                tra.start()
                        
            elif(state.get_system_state() == "land"):
                drone.control_tab.land()
                cv2.destroyAllWindows()
                writer.release()
                break
                #sys.exit(0)
            
            # elif(state.get_airborne()):
            #     lid = threading.Thread(target=distance)
            #     lid.start()
                    
            #print(state.get_system_state(),state.get_airborne())
                      
            writer.write(img)
            #cv2.imshow("Capture",img)
            
            if cv2.waitKey(1) & 0XFF == ord('q'):
               break
            
        except Exception as e:
            print(str(e))
            
    cv2.destroyAllWindows()
    writer.release()
        
        
    
