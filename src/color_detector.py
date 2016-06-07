#!/usr/bin/env python
import roslib
roslib.load_manifest('miniproj')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class BallDetector:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/komodo_1/Asus_Camera/rgb/image_raw", Image, self.callback)
        self.result_pub = rospy.Publisher("/ball_detector", String, queue_size=10)

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, desired_encoding='bgr8')
        except CvBridgeError as e:
            print(e)

        blurred = cv2.GaussianBlur(cv_image, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (-20, 30, 30), (20, 255, 255))
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        res = "%d,%d;%d" % (0, 0, 0)

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            print "found ball at: (%d,%d), radius: %d" % (x, y, radius) #640 X 480

            # only proceed if the radius meets a minimum size
            if radius > 1:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(cv_image, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(cv_image, center, 2, (0, 0, 255), -1)
                res = "%d,%d;%d" % (x, y, radius)

        # publish result
        self.result_pub.publish(String(res))

        # optional: show img (debug)
        cv2.imshow("Image window", cv_image)
        cv2.waitKey(3)


def main():
    rospy.init_node('cv_ball_detector', anonymous=True)
    BallDetector()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
