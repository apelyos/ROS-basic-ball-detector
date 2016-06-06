#!/usr/bin/env python
import roslib; roslib.load_manifest('miniproj')
import rospy
#from std_msgs.msg import String
from geometry_msgs.msg import Twist

def mover():
    rospy.init_node('controller')
    # geometry_msgs/Twist
    pub = rospy.Publisher('/komodo_1/diff_driver/command', Twist)

    rate = rospy.Rate(1) # 1hz

    while not rospy.is_shutdown():
        # substitute the time to the message
        #str = ' Hello ROS World %s ' % rospy.get_time()

        twist = Twist()
        twist.linear.x = -0.2;                   # our forward speed
        #twist.linear.y = 0; twist.linear.z = 0;     # we can't use these!
        #twist.angular.x = 0; twist.angular.y = 0;   #          or these!
        #twist.angular.z = 0;
        rospy.loginfo(str(twist))
        pub.publish(twist)
        rate.sleep()

        twist.linear.x = 0;
        rospy.loginfo(str(twist))
        pub.publish(twist)
        rate.sleep()

if __name__ == '__main__':
    try:
        mover()
    except rospy.ROSInterruptException:
        pass
