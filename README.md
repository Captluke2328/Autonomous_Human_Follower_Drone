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

  
**To run in Actual Drone:**
* Inside "config.py" change SiTL IP address to Pixhawk Connection
  - >From - self.connection_string = '192.168.8.121:14553' --> To - self.connection_string = '/dev/ttyTHS1,921600'

* Run main script:
  - > _sudo python3 main.py_
  
**Run this script under your own Risk**
 
