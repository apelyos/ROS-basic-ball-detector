# Basic ball-detector & mover 
* Course: Topics In Ai And Robotics
* Lecturer: Dr. A. Berler
* Year: 2016 Sems.B
* Ben-Gurion university of the negev

## How to install:
* make sure you have ~/catkin_ws and all the usual ric reqs
* clone https://github.com/robotican/ric into catkin_ws/src/ric
* clone this repo into catkin_ws/src/miniproj
* copy models/3doors to ~/.gazebo/models/
* make sure you have in .bashrc : source ~/catkin_ws/devel/setup.bash
* run: catkin_make 
* run: rospack list, make sure you see "ric" & "miniproj"

## How to launch:
* roslaunch miniproj komodo_3doors.launch - normal position, or:
* roslaunch miniproj komodo_3doors_reverse.launch - robot in reverse position

* Note: the launch files automatically runs the the python scripts:
* color_detector.py
* explorer.py
