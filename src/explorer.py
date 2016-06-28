#!/usr/bin/env python
import roslib

roslib.load_manifest('miniproj')
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

TOLERANCE = 15
OBSTACLE_RANGE = 0.5
IMG_WIDTH = 640

class Explorer:
    has_obstacle = False
    detected_ball = False
    ball_x = 0

    def __init__(self):
        self.laser_sub = rospy.Subscriber("/komodo_1/scan", LaserScan, self.laser_callback)
        self.det_sub = rospy.Subscriber("/ball_detector", String, self.detector_callback)
        self.command_pub = rospy.Publisher('/komodo_1/diff_driver/command', Twist, queue_size=10)

    def laser_callback(self, data):
        # What's the closest laser reading
        closest = min(data.ranges)
        #print "closest %f" % closest
        if closest < OBSTACLE_RANGE:
            self.has_obstacle = True
        else:
            self.has_obstacle = False


    def detector_callback(self, data):
        (cord, radius) = data.data.split(';')
        (x, y) = cord.split(',')

        if int(radius) > 0:
            self.detected_ball = True
            self.ball_x = int(x)
            #print ball_x

    def mover(self, direction, vel = "FAST"):
        twist = Twist()
        twist.linear.x = 0                   # our forward speed
        twist.linear.y = 0
        twist.linear.z = 0     # we can't use these!
        twist.angular.x = 0
        twist.angular.y = 0   #          or these!
        twist.angular.z = 0

        if vel == "FAST":
            velocity = 0.4
        elif vel == "MED":
            velocity = 0.2
        else   :
            velocity = 0.1

        if direction == "LEFT":
            twist.angular.z = velocity
        elif direction == "RIGHT":
            twist.angular.z = -velocity
        elif direction == "STRAIGHT":
            twist.linear.x = velocity
        else : # "STOP" or anything else goes here
            pass

        print "moving, direction: " + direction + " vel: " + str(velocity)
        self.command_pub.publish(twist)


    def main_loop(self):
        rate = rospy.Rate(1) # 1hz
        self.mover("STOP") # init
        #need to init arm to fixed position

        while not rospy.is_shutdown():
            rate.sleep()

            #self.mover("STOP")

            if self.has_obstacle:
                print "obstacle detected, stopping"
                self.mover("STOP")
                continue

            if not self.detected_ball:
                # Scan for ball
                self.mover("RIGHT", "FAST")
                print "scanning for ball: turning"
            else :
                self.mover("STOP")
                #print "found ball"

                offset = (IMG_WIDTH / 2) - self.ball_x
                print "off: %d" % offset
                if abs(offset) < TOLERANCE :
                    self.mover("STRAIGHT")
                else :
                    if offset > 0 :
                        self.mover("LEFT", "SLOW")
                    else :
                        self.mover("RIGHT", "SLOW")


def main():
    rospy.init_node('explorer', anonymous=True)
    explorer = Explorer()
    explorer.main_loop()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")


if __name__ == '__main__':
    main()
