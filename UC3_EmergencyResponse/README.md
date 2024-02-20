# decice_sar

## Name
Cooperative search-and-rescue project.

## Description
ROS project to develop a search-and-rescue use case for the DECICE EU project.

## Requirements
Tested on Ubuntu 20.04.

- [Install ROS2 Foxy](https://docs.px4.io/main/en/ros/ros2_comm.html#install-ros-2)
- [Install PX4](https://docs.px4.io/main/en/ros/ros2_comm.html#install-px4)
- [Setup Micro XRCE-DDS Agent & Client](https://docs.px4.io/main/en/ros/ros2_comm.html#setup-micro-xrce-dds-agent-client)

## Installation
If you do not have a ROS 2 workspace run on a terminal:

```
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```
To install the toolbox clone the repo and mv the use-case 3 root into the src folder of the ROS2 workspace:

```
git clone --recursive --branch uc3 git@gitlab-ce.gwdg.de:decice/decice-wp5.git .
cp -r /path/to/decice-wp5/UC3_EmergencyResponse/* /path/to/ros2_ws/scr
```

Install required Python packages
```
pip3 install -r requirements.txt 
```

## Usage
Run MicroXRCEAgent:

```
MicroXRCEAgent udp4 -p 8888
```
 In a new terminal start PX4 and drone Gazebo simualtion:

```
cd /path/to/PX4_Autopilot
make px4_sitl gazebo-classic
```

In a new terminal build the ros2 toolbox and source:
```
cd path/to/ros2_ws
colcon build
source install/local_setup.zsh
```

Launch the ROS nodes cloud, edge and fc to read coordinates and send the navigation goal to the drone:

```
ros2 launch searche_and_rescue sar_launch.py
```

If it's the first time you check-out a repo you need to use --init first:

```
git submodule update --init --recursive
```