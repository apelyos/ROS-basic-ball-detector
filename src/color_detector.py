#!/usr/bin/env python
import roslib
#roslib.load_manifest('my_package')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

#from __future__ import print_function
import numpy as np



# define the list of boundaries
# pixels in our image in this range considered as red
boundaries = [
	([17, 15, 100], [50, 56, 200]) 
]

#cv_image = 0

class image_converter:

  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/komodo_1/Asus_Camera/rgb/image_raw",Image,self.callback)


  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, desired_encoding='bgr8')
    except CvBridgeError as e:
      print(e)
      
    lower = np.array([17, 15, 100], dtype = "uint8")
    upper = np.array([50, 56, 200], dtype = "uint8") 
      
    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)  
    #cv2.imshow("Image window", cv_image)
    #cv2.waitKey(3)
    
    if cv2.countNonZero(mask) > 0:
      print cv2.countNonZero(mask)


if __name__ == '__main__':
  
  conv = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  
  #rospy.spin()
  #for (lower, upper) in boundaries:
