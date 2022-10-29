# Autonomous_Human_Follower_Drone

**There are two ways on how to run and simulate this program as follow:**
1. Using Gazebo and SITL
2. Using an actual drone

**To run in Simulator:**
* Run this command in Gazebo:
  - >_gazebo --verbose ~/ardupilot_gazebo/worlds/iris_arducopter_runway.world_
* Run this command in SiTL:
  - >_cd ~/ardupilot/ArduCopter/_
  - >_sim_vehicle.py -v ArduCopter -f gazebo-iris --console --out 192.168.195.204:14553_
  - > **Note** : "192.168.195.204:14553" is referring to JetsonNano or RPI address of our drone

* Run main script:
  - > _sudo python3 main.py_
  
* Sample Output:
<img width="1413" alt="image" src="https://user-images.githubusercontent.com/81543946/197373289-b8bd8f86-546d-46da-9581-531374bb337e.png">

  
**To run in Actual Drone:**
* Inside "config.py" change SiTL IP address to Pixhawk Connection
  - >From - self.connection_string = '192.168.8.121:14553' --> To - self.connection_string = '/dev/ttyTHS1,921600'

* Run main script:
  - > _sudo python3 main.py_
  
* Configure Jetson Nano by disabling GUI and Save RAM
  * Disable GUI to free up more RAM
  - > sudo systemctl set-default multi-user
    
   * Disable ZRAM
  - > sudo systemctl disable nvzramconfig.service
  
   * Default to Max-N power mode
  - > sudo nvpmodel -m 0
  
 * Configure Jetson Nano to enable GUI again
    * Re-enable GUI
   - > sudo systemctl set-default graphical.target

  
**Run this script under your own Risk**
 
